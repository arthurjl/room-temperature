import pyautogui

from datetime import datetime


def take_screenshot():
  filename = datetime.now().strftime("%Y%m%d-%H%M%S")
  myScreenshot = pyautogui.screenshot()
  print(myScreenshot)
  myScreenshot.save(f'backend\screenshots\{filename}.png')

if __name__ == "__main__":
  take_screenshot()