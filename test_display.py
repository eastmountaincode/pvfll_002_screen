#!/usr/bin/env python3
"""
Hardware display test — run on the Pi to push a test layout to the e-ink screen.
Usage: python3 test_display.py
"""

from display import init_display, display_boxes, load_file_icon, sleep_display

load_file_icon()
init_display()

test_data = {
    1: {"empty": True},
    2: {"empty": False, "name": "photo.jpg", "type": "Image", "size": 1234567},
    3: {"empty": False, "name": "long_filename_here.pdf", "type": "PDF", "size": 987654},
    4: {"empty": True},
}

display_boxes(test_data, force_full=True)
sleep_display()
print("Done.")
