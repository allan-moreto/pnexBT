import pyautogui
import time
import random
import threading
from pynput import keyboard
from pynput.keyboard import Controller
import os
keyboard_controller = Controller()

running = True  # Flag global

fight_location = (1317, 658, 48, 26)
run_location = (1457, 709, 45, 26)
curr_mouse_location = fight_location
request_path = "./win_assets/request.png"
cancel_request_location = (1526, 595, 68, 25)

time.sleep(5)
def auto_click():
    global running
    while running:
        pyautogui.click()
        time.sleep(0.3)


def move_left_right():
    global running
    while running:
        # Hold LEFT
        keyboard_controller.press('a')
        time.sleep(random.uniform(0.3, 0.6))
        keyboard_controller.release('a')

        # Hold RIGHT
        keyboard_controller.press('d')
        time.sleep(random.uniform(0.3, 0.6))
        keyboard_controller.release('d')

def on_press(key):
    global running
    try:
        if key == keyboard.Key.esc:
            print("⛔ ESC pressionado, parando...")
            running = False
            return False  # Para o listener
    except:
        pass


def click(region):
    # OR click at a random point inside the region
    x = region[0] + region[2] // 2
    y = region[1] + region[3] // 2
    time.sleep(random.randint(2, 4))
    pyautogui.click(x, y)
    time.sleep(0.5)


def take_screenshot(region=None, folder="screenshots"):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Find the next available filename
    index = 1
    while True:
        filename = os.path.join(folder, f"screenshot_{index}.png")
        if not os.path.exists(filename):
            break
        index += 1

    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filename)
    print(f"✅ Screenshot saved to {filename}")
    return filename

def watch_screen():
    global running
    while running:
        try:
            # special_pokemon = pyautogui.locateAllOnScreen()
            request = pyautogui.locateOnScreen(request_path, confidence=0.9)
            special_pokemon = pyautogui.locateOnScreen()
            if request:
                take_screenshot((1315, 462, 291, 117))
                time.sleep(2)
                click(cancel_request_location)
                time.sleep(4)
                pyautogui.moveTo(curr_mouse_location)
                time.sleep(random.randint(4, 6))
        except pyautogui.ImageNotFoundException:
            continue

# Thread para ouvir o teclado
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Thread do clique automático
click_thread = threading.Thread(target=auto_click, daemon=True)
click_thread.start()

# Screen watching thread
watch_thread = threading.Thread(target=watch_screen, daemon=True)
watch_thread.start()

# Movimento no thread principal
move_left_right()
