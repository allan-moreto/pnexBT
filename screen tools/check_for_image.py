import time
import pyautogui
from win_assets.image_regions import fight_img_region

time.sleep(3)

def is_image_present(image_path, region=None, confidence=0.9):
    """
    Checks if the given image exists on the screen (or in a region).
    
    Parameters:
    - image_path: str, path to the image file
    - region: tuple (x, y, width, height), optional search area
    - confidence: float, 0.0-1.0 confidence threshold
    
    Returns:
    - True if image found, False otherwise
    """
    try:
        image = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        return image
    except Exception as e:
        print(f"Error detecting image: {e}")
        return False

# Example usage
if __name__ == "__main__":
 # Path to your image
    IMAGE_PATH = "./win_assets/fight.png"

# Optional: define a region to limit search (x, y, width, height)
    SEARCH_REGION = fight_img_region
    
    if is_image_present(IMAGE_PATH, region=SEARCH_REGION):
        print("image detected")
    else:
        print("Image not detected.")
