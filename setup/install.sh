#!/bin/bash
set -e

# Captive portal setup for pvfll_002
# Run once on a fresh Pi: sudo bash setup/install.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== pvfll_002 captive portal setup ==="

# 1. Install dependencies
echo "[1/5] Installing packages..."
apt install -y dnsmasq python3-flask

# 2. Stop system dnsmasq from interfering (we run our own instance)
echo "[2/5] Configuring dnsmasq..."
systemctl stop dnsmasq
systemctl disable dnsmasq

# 3. Create NetworkManager AP connection profile
echo "[3/5] Creating AP connection profile..."
# Remove if it already exists
nmcli con delete pvfll-portal 2>/dev/null || true
nmcli con add type wifi ifname wlan1 mode ap con-name pvfll-portal \
    ssid "pvfll_002" \
    ipv4.method shared \
    ipv4.addresses 192.168.4.1/24 \
    wifi-sec.key-mgmt wpa-psk \
    wifi-sec.psk "htmlpg2025"

# 4. Install service files and config
echo "[4/5] Installing systemd services..."
cp "$SCRIPT_DIR/portal-interface.service" /etc/systemd/system/
cp "$SCRIPT_DIR/portal-dnsmasq.service" /etc/systemd/system/
cp "$SCRIPT_DIR/portal-web.service" /etc/systemd/system/

mkdir -p /etc/dnsmasq.d
cp "$SCRIPT_DIR/portal-dnsmasq.conf" /etc/dnsmasq.d/portal.conf

# 5. Enable and start services
echo "[5/5] Enabling services..."
systemctl daemon-reload
systemctl enable portal-interface portal-dnsmasq portal-web
systemctl start portal-interface
sleep 2
systemctl start portal-dnsmasq portal-web

echo ""
echo "=== Done! ==="
echo "AP SSID:     pvfll_002"
echo "AP Password: htmlpg2025"
echo "Portal URL:  http://192.168.4.1"
echo ""
echo "Connect to the 'pvfll_002' WiFi network from your phone to configure."
