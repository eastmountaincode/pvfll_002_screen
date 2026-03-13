import time
from display import (
    init_display, display_boot_splash, display_centered_message,
    display_portal_message, load_file_icon,
    BOOT_SPLASH, BOOT_BEES, BOOT_BUTTERFLY, BOOT_PSYCHIC, BOOT_YOYO,
)
from util import is_wifi_connected
from api import fetch_all_boxes
from pusher_events import PusherListener

WIFI_RETRY_INTERVAL = 10  # seconds between WiFi checks
BOOT_MSG_MIN_SECONDS = 1.5  # minimum time each boot screen stays visible

_last_boot_msg_time = 0


def boot_msg(message: str, img_id: str = BOOT_SPLASH):
    """Display a boot message with illustration, enforcing minimum display time."""
    global _last_boot_msg_time
    elapsed = time.monotonic() - _last_boot_msg_time
    if _last_boot_msg_time > 0 and elapsed < BOOT_MSG_MIN_SECONDS:
        time.sleep(BOOT_MSG_MIN_SECONDS - elapsed)
    display_boot_splash(message, img_id)
    _last_boot_msg_time = time.monotonic()


def boot_sequence() -> tuple:
    """
    Boot sequence:
      1. Initialize display + load file icon
      2. Check Wi-Fi connectivity (wait with portal message if not connected)
      3. Connect to Pusher WebSocket
      4. Fetch initial box data
    Returns (box_data, pusher_listener) or (None, None) on failure.
    """

    # Step 1: Initialize display
    try:
        init_display()
        load_file_icon()
        boot_msg("Booting...", BOOT_SPLASH)
    except Exception as e:
        print(f"Error initializing display: {e}")
        return None, None

    # Step 2: Check Wi-Fi — show portal instructions and retry until connected
    boot_msg("Checking Wi-Fi...", BOOT_PSYCHIC)
    if not is_wifi_connected():
        print("No Wi-Fi — showing captive portal instructions")
        display_portal_message()
        while not is_wifi_connected():
            time.sleep(WIFI_RETRY_INTERVAL)
        print("Wi-Fi connected!")
        boot_msg("Wi-Fi connected!", BOOT_BUTTERFLY)

    # Step 3: Connect to Pusher
    boot_msg("Connecting WebSocket...", BOOT_YOYO)
    pusher_listener = PusherListener()
    if pusher_listener.connect():
        print("WebSocket connected")
    else:
        display_centered_message("WebSocket failed", font_size=24)
        print("Failed to connect to WebSocket")
        return None, None

    # Step 4: Fetch initial data
    boot_msg("Fetching data...", BOOT_BEES)
    try:
        box_data = fetch_all_boxes()
        boot_msg("Boot complete!", BOOT_BUTTERFLY)
        time.sleep(3)
        return box_data, pusher_listener
    except Exception as e:
        display_centered_message("Data fetch failed", font_size=24)
        print(f"Error fetching data: {e}")
        return None, None
