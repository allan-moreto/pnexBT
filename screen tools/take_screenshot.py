import pyautogui
import time

time.sleep(10)

screenshot = pyautogui.screenshot()
screenshot.save("./assets/test.png")

