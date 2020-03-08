from _ast import arg

import pyautogui
import win32gui
import win32con
from pynput import keyboard

def defineCanvas():
    # v2 - hidden taskbar?
    taskbarWidth = 0
    taskbarHandle = win32gui.FindWindow("shell_traywnd", None)
    taskbarRect = win32gui.GetWindowRect(taskbarHandle)
    pyautogui.size()        # 0 = 3840, 1 = 2160

    if taskbarRect[0] == taskbarRect[1] == 0:
        print("top or left")
        if taskbarRect[2] == pyautogui.size()[0]:
            print("top -> " , taskbarRect)
            taskbarWidth = taskbarRect[3] - taskbarRect[1]
            # define canvas
            canvasRect = (0,taskbarWidth,pyautogui.size()[0], pyautogui.size()[1])
            print("canvasRect tuple : ", canvasRect)
            return canvasRect
        if taskbarRect[3] == pyautogui.size()[1]:
            print("left -> ", taskbarRect)
            taskbarWidth = taskbarRect[2] - taskbarRect[0]
            canvasRect = (taskbarWidth,0,pyautogui.size()[0], pyautogui.size()[1])
            print("canvasRect tuple : ", canvasRect)
            return canvasRect

    if taskbarRect[2] == pyautogui.size()[0] and taskbarRect[3] == pyautogui.size()[1]:
        print("bottom or right")
        if taskbarRect[0] == 0:
            print("bottom -> ", taskbarRect)
            taskbarWidth = taskbarRect[3] - taskbarRect[1]
            # define canvas
            canvasRect = (0, 0, pyautogui.size()[0], pyautogui.size()[1]-taskbarWidth)
            print("canvasRect tuple : ", canvasRect)
            return canvasRect
        if taskbarRect[1] == 0:
            print("right -> ", taskbarRect)
            taskbarWidth = taskbarRect[2] - taskbarRect[0]
            # define canvas
            canvasRect = (0, 0, pyautogui.size()[0] - taskbarWidth, pyautogui.size()[1])
            print("canvasRect tuple : ", canvasRect)
            return canvasRect

# staic window rect starting point, variable window rect ending point
def windowStats():
    print("entered windowStats")
    # current position and dimensions
    tempHandle = win32gui.GetForegroundWindow()
    windowRect = win32gui.GetWindowRect(tempHandle)     ## (0,0,0,0)
    windowRect_X = windowRect[0]
    windowRect_Y = windowRect[1]
    windowRect_height = windowRect[3] - windowRect[1]
    windowRect_width = windowRect[2] - windowRect[0]

    # formating tupple
    statsOut = (tempHandle, windowRect_X, windowRect_Y, windowRect_width, windowRect_height)

    print(statsOut)
    return statsOut


def gridOperation(argList):
    winStats = list(windowStats())
    if argList[2] == '+':
        winStats[argList[0]] += argList[1]
    elif argList[2] == '-':
        winStats[argList[0]] -= argList[1]
    win32gui.SetWindowPos(winStats[0], win32con.HWND_NOTOPMOST, winStats[1], winStats[2], winStats[3], winStats[4], 0)

def on_press(key):
    try: k = key.char                           # single-char keys
    except: k = key.name                        # other keys
    if key == keyboard.Key.esc: return False    # stop listener

    if k in list(dictGrid.keys()):              # keys interested
        # self.keys.append(k)                   # store it in global variable
        gridOperation(dictGrid[k])
        print('Key pressed: ' + k)
        # return False # remove this if want more keys
    else:
        print('Key pressed: ' + key.char)


########################## MAIN  ######################################
gridColumns = input("Grid Colums: ")
gridRows = input("Grid Rows: ")
canvasRect = defineCanvas()
stepColumn = int((canvasRect[2] - canvasRect[0])/int(gridColumns))
stepRow = int((canvasRect[3] - canvasRect[1])/int(gridRows))

dictGrid = {
    # size
    'w': [4, stepRow, '-'],
    's': [4, stepRow, '+'],
    'a': [3, stepColumn, '-'],
    'd': [3, stepColumn, '+'],

    # position
    'up': [2, stepRow, '-'],
    'down': [2, stepRow, '+'],
    'left': [1, stepColumn, '-'],
    'right': [1, stepColumn, '+']
}

print("entering listener")
# listener
lis = keyboard.Listener(on_press = on_press, suppress = True)
lis.start() # start to listen on a separate thread
lis.join() # no this if main thread is polling self.keys


############################
############################

#### win32con.HWND_TOPMOST -> always on top
### use for za ''highlight active'' feature

############################
############################
