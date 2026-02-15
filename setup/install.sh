#!/bin/bash
set -e

# Captive portal setup for pvfll_002
# Run once on a fresh Pi: sudo bash setup/install.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== pvfll_002 captive portal setup ==="

# 1. Install dependencies (dnsmasq-base is already pulled by NM shared mode)
echo "[1/4] Installing packages..."
apt install -y python3-flask

# 2. Create NetworkManager AP connection profile
echo "[2/4] Creating AP connection profile..."
nmcli con delete pvfll-portal 2>/dev/null || true
nmcli con add type wifi ifname wlan1 mode ap con-name pvfll-portal \
    ssid "pvfll_002" \
    ipv4.method shared \
    ipv4.addresses 192.168.4.1/24 \
    802-11-wireless-security.key-mgmt wpa-psk \
    802-11-wireless-security.psk "htmlpg2025"

# 3. DNS hijack config — NM's shared dnsmasq reads from this directory
echo "[3/4] Configuring DNS hijack..."
cp "$SCRIPT_DIR/portal-dnsmasq.conf" /etc/NetworkManager/dnsmasq-shared.d/portal.conf

# 4. Install and start systemd services
echo "[4/4] Installing systemd services..."
cp "$SCRIPT_DIR/portal-interface.service" /etc/systemd/system/
cp "$SCRIPT_DIR/portal-web.service" /etc/systemd/system/

# Remove old dnsmasq service if it was installed previously
systemctl disable portal-dnsmasq 2>/dev/null || true
rm -f /etc/systemd/system/portal-dnsmasq.service

systemctl daemon-reload
systemctl enable portal-interface portal-web
systemctl restart portal-interface
sleep 2
systemctl restart portal-web

echo ""
echo "=== Done! ==="
echo "AP SSID:     pvfll_002"
echo "AP Password: htmlpg2025"
echo "Portal URL:  http://192.168.4.1"
echo ""
echo "Connect to the 'pvfll_002' WiFi network from your phone to configure."
