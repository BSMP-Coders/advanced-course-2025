#!/bin/bash

echo "🔍 Testing VNC Setup..."
echo "=========================="

# Test 1: Check if VNC processes are running
echo "1. Checking VNC processes..."
ps aux | grep -E "(Xvfb|fluxbox|x11vnc|websockify)" | grep -v grep
if [ $? -eq 0 ]; then
    echo "✅ VNC processes found"
else
    echo "❌ No VNC processes running"
fi

echo ""

# Test 2: Check if ports are listening
echo "2. Checking ports..."
netstat -tlnp | grep -E "(5900|6080)"
if [ $? -eq 0 ]; then
    echo "✅ VNC ports are listening"
else
    echo "❌ VNC ports not listening"
fi

echo ""

# Test 3: Check if display is available
echo "3. Testing X display..."
if [ -f ".venv/bin/python" ]; then
    DISPLAY=:1 .venv/bin/python -c "import pygame; pygame.init(); pygame.display.set_mode((100, 100)); print('Display test passed')" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ X display :1 is available for pygame"
    else
        echo "❌ X display :1 not available for pygame"
    fi
else
    echo "❌ Cannot test display - virtual environment not found"
fi

echo ""

# Test 4: Check Python environment
echo "4. Testing Python environment..."
if [ -f ".venv/bin/python" ]; then
    echo "✅ Virtual environment exists"
    .venv/bin/python -c "import pygame; print('✅ Pygame imported successfully')" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Pygame is installed and working"
    else
        echo "❌ Pygame not working"
    fi
else
    echo "❌ Virtual environment not found"
fi

echo ""

# Test 5: Check VNC web interface
echo "5. Testing VNC web interface..."
curl -s http://localhost:6080 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ VNC web interface accessible"
else
    echo "❌ VNC web interface not accessible"
fi

echo ""
echo "🎮 Test complete! If all tests pass, you're ready to run your games!"
echo "🌐 Access VNC at: http://localhost:6080/vnc.html"
