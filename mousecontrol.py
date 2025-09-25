import pyautogui


def main():
    screenWidth,screenHeight = pyautogui.size()
    print(f'Screen Width: {screenWidth} , Screen Height: {screenHeight}')
    pyautogui.moveTo(screenWidth/2,screenHeight/2,duration=2)
    pyautogui.click()
    pyautogui.click(button='right')
    pyautogui.click(clicks=2)



if __name__ == '__main__':
    main()
