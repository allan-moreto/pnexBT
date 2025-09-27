# grinding.py
import pyautogui, time, random, threading, os, pyscreeze, winsound, requests, asyncio
from pynput.keyboard import Controller
from PIL import Image

pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
WEBHOOK_URL = "https://discord.com/api/webhooks/1419970299063177218/ZKqbHO5hSNrfamc3jxKXxyYEO-Uw206xgdAyRaUjvI944yIgfak_SHixIGpJBZEawCKE"
kb = Controller()
pause_event = threading.Event()
running = False  # flag
walking = True

fight_location = (1317, 658, 48, 26)
run_location = (1457, 709, 45, 26)
curr_mouse_location = fight_location
request_path = "../win_assets/request.png"
elite_path = "../win_assets/elite.png"
elite_region = (1611, 280, 57, 70)
handle_request_location = (1526, 595, 68, 25)
alarm_active = True
move_num = "1"
catch_synch_bool = True
battle_elite_bool = False
use_sweeper_bool = False

def run():
    print("running away from ELITE")
    time.sleep(4)
    key_press("4")
    time.sleep(0.05)
    key_press("4")
    time.sleep(4)

def catch_pokemon():
    global walking
    print("catching pokemon")
    walking = False
    time.sleep(10)
    walking = True
    # while loop that throws some balls until battle image has dissapeared,
    # should throw balls, use potions, use false swipe, do a screen_sweep
    # after thrown ball and time.sleep


def battle_elite():
    global walking
    walking = False
    print("battling elite")
    time.sleep(10) 
    walking = True

def sweeper_battle():
    global walking
    walking = False
    print("battling with sweeper")
    time.sleep(10) 
    walking = True

def handle_special():
    global running
    print("handling special encounter")
    running = False
    if alarm_active: winsound.Beep(1000, 3000)
    send_discord_alert("you've got a special pokemon!")
    time.sleep(30)
    pyautogui.hotkey("ctrl", "r")

def send_message(message):
    time.sleep(3)
    stop_grinding()
    pause_event.clear()
    time.sleep(5)
    pyautogui.moveTo(1548, 974)
    time.sleep(0.5)
    pyautogui.click(1548, 974)
    pyautogui.click(1548, 974)
    pyautogui.write(message)
    time.sleep(1)
    pyautogui.moveTo(1834, 974)
    time.sleep(0.5)
    pyautogui.click(1834, 974)
    pyautogui.click(1834, 974)
    time.sleep(3)
    pause_event.set()
    start_grinding()

def handle_request():
    if alarm_active: winsound.Beep(1000, 3000)
    pause_event.clear()
    filename = take_screenshot((1315, 462, 291, 117))
    send_discord_alert("you've got a player request!", filename)
    time.sleep(2)
    click(handle_request_location)
    time.sleep(random.randint(4, 6))
    pause_event.set()

def battle(move_num):
    time.sleep(0.3)
    key_press("1")
    time.sleep(0.1)
    key_press(move_num)
    time.sleep(3)

def send_discord_alert(text, filename=None):
    payload = {"content": text}
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    if filename:
        with open(filename, "rb") as f:
            payload = {"content": "📸 Screenshot from the bot!"}
            files = {"file": f}
            response = requests.post(WEBHOOK_URL, data=payload, files=files)
            if response.status_code == 204:
                print("✅ Screenshot sent successfully to Discord")
            else:
                print(f"⚠️ Failed to send screenshot: {response.status_code}, {response.text}")
    return resp

def handle_pm():
    pause_event.clear()
    filename = take_screenshot((1405, 778, 492, 182))
    send_discord_alert("you've got a private message", filename)
    time.sleep(1)
    pyautogui.moveTo(1548, 974)
    time.sleep(0.5)
    pyautogui.click(1548, 974)
    pyautogui.click(1548, 974)
    time.sleep(1)
    pyautogui.write("/lle")
    time.sleep(1)
    pyautogui.moveTo(1834, 974)
    time.sleep(0.5)
    pyautogui.click(1834, 974)
    pyautogui.click(1834, 974)
    time.sleep(1)
    pause_event.set()
    print("starting back grind")


on_screen = {
    "battle": [False, "../win_assets/battle.png"],
    "battle_elite": [False, "../win_assets/elite.png"], 
    "handle_request": [False, "../win_assets/handle_request.png"], 
    "catch_synch": [False, "../win_assets/synch.png"], 
    "handle_special": [False, "../win_assets/handle_special.png"],
    "handle_pm": [False, "../win_assets/handle_pm.png"],
    "golem": [False, "../win_assets/golem.png"],
    "magnemite": [False, "../win_assets/magnemite.png"],
    "sandslash": [False, "../win_assets/sandslash.png"],
    "magcargo": [False, "../win_assets/magcargo.png"],
    
    
    # maybe set keys for catch_pokeName and run_pokeName then if key.contains catch or run do something
}
images = {
    "battle_elite": "../win_assets/elite.png",
    "cancel_request": "../win_assets/request.png",
    "catch_synch": "../win_assets/synch.png",
    "handle_special": "../win_assets/special.png",
    "battle": "../win_assets/battle.png",
    "handle_pm": "../win_assets/handle_pm.png"
}
func_map = {
    "catch_synch": catch_synch,
    "cancel_request": cancel_request,
    "handle_special": handle_special,
    "battle_elite": battle_elite,
    "battle": lambda: battle(move_num),
    "handle_pm": handle_pm
}
move_map = {}

preloaded_templates = {name: Image.open(path) for name, path in images.items()}

def reload_images():
    global preloaded_images
    preloaded_images = {name: Image.open(path[1]) for name, path in on_screen.items()}

def key_press(key):
    kb.press(key)
    time.sleep(0.05)
    kb.release(key)

def move_left_right():
    global running, walking
    while running:  # keep thread alive as long as running
        pause_event.wait()

        if not walking:
            time.sleep(0.1)  # avoid busy-wait
            continue

        # Randomly choose starting direction
        directions = ['a', 'd']
        if random.random() < 0.5:
            directions.reverse()  # 50% chance to swap order

        for key in directions:
            kb.press(key)
            time.sleep(random.uniform(0.3, 0.6))
            kb.release(key)

def isolate_func(func_name):
    pause_event.clear()
    func_name()
    pause_event.set()

def sweep_screen(confidence=0.9):
    screenshot = pyautogui.screenshot(region=(1263, 302, 537, 689)) 
    for name, template in preloaded_images.items():
        location = pyautogui.locate(template, screenshot, confidence=confidence)
        on_screen[name][0] = bool(location)
    
def watch_screen():
    global running, walking
    while running:
        pause_event.wait()

        # Update on_screen with latest results
        sweep_screen()

        if on_screen["handle_pm"][0]:
            handle_pm()
        if on_screen["handle_special"][0]:
            handle_special()
        if on_screen["handle_request"][0]:
            handle_request()

        if on_screen["battle_elite"][0] and battle_elite_bool:
            battle_elite()
        elif on_screen["battle_elite"][0] and not battle_elite_bool:
            run()

        catch_mon = next((pokemon for pokemon in catch_mons if on_screen.get(pokemon, [False])[0]),None)
        if catch_mon and not catch_synch_bool:
            catch_pokemon()
            continue
        elif catch_mon and catch_synch_bool:
            if on_screen["catch_synch"][0]:
                catch_pokemon()
                continue
        
        current_pokemon = next((pokemon for pokemon in dinamic_pokemon if on_screen.get(pokemon, [False])[0]),None)
        if current_pokemon == None:
            time.sleep(0.1)
            sweep_screen()
            current_pokemon = next((pokemon for pokemon in dinamic_pokemon if on_screen.get(pokemon, [False])[0]),None)

        move_num = move_map[current_pokemon]

        if on_screen["battle"][0]:
            walking = False
            if not use_sweeper_bool:
                while on_screen["battle"][0]:
                    print(f"cuurent pokemon is: {current_pokemon}")
                    print(f"dimanic pokemons list: {dinamic_pokemon}")
                    battle(move_num)
                    sweep_screen()
            else:
                sweeper_battle()
        else:
            walking = True
        time.sleep(0.2)

def click(region):
    x = region[0] + region[2] // 2
    y = region[1] + region[3] // 2
    time.sleep(random.randint(2, 4))
    pyautogui.click(x, y)
    time.sleep(0.5)

def take_screenshot(region=None, folder="screenshots"):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"screenshot_{int(time.time())}.png")
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filename)
    print(f"✅ Screenshot saved to {filename}")
    return filename

def get_grindind_input_data(grinding_data):
    print(grinding_data)
    return grinding_data

def timer_cycle(session_time: int, run_time: int, break_time: int):
    start_time = time.time()
    elapsed = 0
    print(f"total session time: {session_time}")
    while elapsed < session_time:
        start_grinding()
        print(f"running for {run_time} seconds")
        time.sleep(run_time)
        elapsed = time.time() - start_time
        if elapsed >= session_time:
            break

        stop_grinding()
        print(f"stopping for {break_time} seconds")
        time.sleep(break_time)
        elapsed = time.time() - start_time
    stop_grinding()
    pyautogui.shortcut("ctrl", "r")

# --- Control functions for GUI ---
threads = []

def start_grinding():
    global running, threads1
    if running:
        print("⚠️ Already running")
        return
    running = True
    print("▶️ Starting grind...")

    # threads
    watch_thread = threading.Thread(target=watch_screen, daemon=True)
    move_thread = threading.Thread(target=move_left_right, daemon=True)


    pause_event.set()
    

    threads = [watch_thread, move_thread]
    for t in threads:
        t.start()

def stop_grinding():
    global running
    if not running:
        print("⚠️ Not running")
        return
    print("⛔ Stopping grind...")
    running = False
