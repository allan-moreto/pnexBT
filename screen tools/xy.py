import pyautogui
import time

print("Move your mouse to the spot you want. Ctrl+C to stop.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x}, Y: {y}", end="\r")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nDone.")