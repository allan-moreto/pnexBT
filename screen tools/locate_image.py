import pyautogui
import time

time.sleep(4)

# Path to your own sprite image
my_sprite_path = ("../win_assets/chat_region.png")

# Locate your sprite on the screen
sprite_location = pyautogui.locateOnScreen(my_sprite_path, confidence=0.9)

if sprite_location:
    print(f"My sprite found at: {sprite_location}")
else:
    print("Could not find my sprite!")
