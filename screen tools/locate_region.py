import pyautogui
import time
import pyautogui
from PIL import ImageDraw
from win_assets.image_regions import fight_img_region

time.sleep(2)
screen_region = (1506, 934, 1506+ 56, 934+53)


# Take a screenshot
screenshot = pyautogui.screenshot()
# Coordinates of detected image (example from locateOnScreen)
# If using pyautogui.locateOnScreen, this will be a box: left, top, width, height
# location = pyautogui.locateOnScreen("./assets/search_images/fight.png")

# Create a drawing object
draw = ImageDraw.Draw(screenshot)

# Draw a red rectangle around detected image
# if location:
#     x, y, w, h = location
#     draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
#     print("Drew rectangle around detected image!")


# Draw a rectangle around a custom area you choose
custom_area = (screen_region)  # (left, top, right, bottom)
draw.rectangle(custom_area, outline="blue", width=3)


# Save the image with rectangles
screenshot.save("screenshot_with_boxes.png")
print("Saved screenshot_with_boxes.png")

