sudo apt-get update && sudo apt-get install -y x11vnc xvfb fluxbox novnc python3-websockify dbus-x11 x11-utils && pip install -r requirements.txt

chmod +x ./admin/start_vnc.sh && ./admin/start_vnc.sh