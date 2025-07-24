#!/bin/bash

# Set up signal handling and process group
set -m  # Enable job control
trap 'echo "Script interrupted"; exit 1' INT TERM

# Start dbus service first
echo "Starting dbus service..."
sudo service dbus start

# Kill any existing VNC processes
pkill -f "Xvfb|fluxbox|x11vnc|websockify" 2>/dev/null

# Remove X server lock files
sudo rm -f /tmp/.X1-lock /tmp/.X11-unix/X1 2>/dev/null

# Wait a moment for cleanup
sleep 2

# Start services in sequence with nohup for persistence
echo "Starting Xvfb..."
export DISPLAY=:1
nohup Xvfb :1 -screen 0 1024x768x24 > /tmp/xvfb.log 2>&1 &
XVFB_PID=$!

sleep 3

echo "Starting fluxbox..."
nohup env DISPLAY=:1 fluxbox > /tmp/fluxbox.log 2>&1 &
FLUXBOX_PID=$!

sleep 2

echo "Starting x11vnc..."
# Wait for Xvfb to be fully ready
for i in {1..10}; do
    if DISPLAY=:1 xdpyinfo >/dev/null 2>&1; then
        echo "Display :1 is ready"
        break
    fi
    echo "Waiting for display :1 to be ready... (attempt $i/10)"
    sleep 1
done

# Start x11vnc with retry logic and better stability
for i in {1..3}; do
    # Kill any existing x11vnc processes first
    pkill -f "x11vnc" 2>/dev/null || true
    sleep 2
    
    # Start x11vnc with more stable options and better signal handling
    nohup x11vnc -display :1 -nopw -listen localhost -forever -shared -rfbport 5900 -noipv6 -noxdamage -bg -o /tmp/x11vnc.log > /dev/null 2>&1 &
    
    # Wait for x11vnc to start and create the port
    sleep 3
    
    # Find the actual x11vnc PID
    X11VNC_PID=$(pgrep -f "x11vnc.*:1")
    
    if [ -n "$X11VNC_PID" ]; then
        # Give it more time to fully initialize
        sleep 5
        
        # Check if x11vnc process is still running AND listening on port 5900
        if kill -0 $X11VNC_PID 2>/dev/null && netstat -tlnp 2>/dev/null | grep -q ":5900.*LISTEN"; then
            echo "x11vnc successfully started and listening on port 5900 (PID: $X11VNC_PID)"
            break
        else
            echo "x11vnc started but not listening properly, retrying... (attempt $i/3)"
            kill $X11VNC_PID 2>/dev/null || true
            sleep 2
        fi
    else
        echo "x11vnc failed to start, retrying... (attempt $i/3)"
        sleep 2
    fi
done

# If x11vnc still failed, try alternative startup method
if [ -z "$X11VNC_PID" ] || ! kill -0 $X11VNC_PID 2>/dev/null || ! netstat -tlnp 2>/dev/null | grep -q ":5900.*LISTEN"; then
    echo "Trying alternative x11vnc startup method..."
    pkill -f "x11vnc" 2>/dev/null || true
    sleep 2
    
    # Try without -bg flag and let nohup handle backgrounding
    DISPLAY=:1 nohup x11vnc -nopw -listen localhost -forever -shared -rfbport 5900 -noipv6 -repeat > /tmp/x11vnc.log 2>&1 &
    X11VNC_PID=$!
    
    sleep 5
    
    if kill -0 $X11VNC_PID 2>/dev/null && netstat -tlnp 2>/dev/null | grep -q ":5900.*LISTEN"; then
        echo "Alternative x11vnc method successful (PID: $X11VNC_PID)"
    else
        echo "ERROR: All x11vnc startup methods failed!"
        echo "Check /tmp/x11vnc.log for details"
    fi
fi

echo "Starting websockify..."
# Make sure x11vnc is ready before starting websockify
for i in {1..10}; do
    if kill -0 $X11VNC_PID 2>/dev/null && netstat -tlnp 2>/dev/null | grep -q ":5900.*LISTEN"; then
        echo "x11vnc port 5900 is ready for websockify"
        break
    fi
    echo "Waiting for x11vnc port 5900... (attempt $i/10)"
    sleep 2
done

# Double-check that x11vnc is still running before starting websockify
if ! kill -0 $X11VNC_PID 2>/dev/null; then
    echo "ERROR: x11vnc process died unexpectedly!"
    exit 1
fi

nohup websockify --web /usr/share/novnc --heartbeat=30 6080 localhost:5900 > /tmp/websockify.log 2>&1 &
WEBSOCKIFY_PID=$!

# Verify websockify started correctly
sleep 3
if netstat -tlnp 2>/dev/null | grep -q ":6080.*LISTEN"; then
    echo "websockify successfully started and listening on port 6080"
else
    echo "Warning: websockify may not have started correctly"
fi

echo "VNC services started!"
echo "Xvfb PID: $XVFB_PID"
echo "Fluxbox PID: $FLUXBOX_PID" 
echo "x11vnc PID: $X11VNC_PID"
echo "Websockify PID: $WEBSOCKIFY_PID"
echo ""

# Final verification
echo "Final verification:"
if kill -0 $X11VNC_PID 2>/dev/null && netstat -tlnp 2>/dev/null | grep -q ":5900.*LISTEN"; then
    echo "✅ VNC server (port 5900) is listening and process is alive"
else
    echo "❌ VNC server (port 5900) is NOT working properly"
    echo "x11vnc process status:"
    if kill -0 $X11VNC_PID 2>/dev/null; then
        echo "  Process is running (PID: $X11VNC_PID)"
    else
        echo "  Process is dead or not found"
    fi
    echo "Port 5900 status:"
    netstat -tlnp 2>/dev/null | grep ":5900" || echo "  Port 5900 not listening"
    echo "Recent x11vnc log:"
    tail -10 /tmp/x11vnc.log 2>/dev/null || echo "  No log file found"
fi

if netstat -tlnp 2>/dev/null | grep -q ":6080.*LISTEN"; then
    echo "✅ Web interface (port 6080) is listening"
else
    echo "❌ Web interface (port 6080) is NOT listening"
fi

echo ""
if [ -n "$CODESPACE_NAME" ] && [ -n "$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN" ]; then
    echo "Access the desktop at: https://$CODESPACE_NAME-6080.$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN/vnc.html"
else
    echo "Access the desktop at: http://localhost:6080/vnc.html"
fi
echo ""
echo "To stop all services, run: pkill -f \"Xvfb|fluxbox|x11vnc|websockify\""
