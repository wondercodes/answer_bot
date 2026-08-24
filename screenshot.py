import pyautogui


def capture_screen():

    print("正在截取屏幕...")

    image = pyautogui.screenshot()

    return image