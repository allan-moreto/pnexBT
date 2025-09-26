import pyautogui
import time

time.sleep(1)

pyautogui.PAUSE = 0.04
pyautogui.moveTo(1417, 588)
time.sleep(1)

clicks = 1500
start = time.time()

for i in range (clicks):
    pyautogui.click(1417, 588)

end = time.time()
elapsed = end - start
cps = clicks / elapsed

print(f"completed {clicks} clicks in {elapsed} seconds, with an average of {cps:.2f} cps")
