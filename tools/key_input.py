import random
import time
import win32api
import win32gui

import win32con


def keyHwnd(hwndEx, char):
    """
    向指定控件输入值
    :param hwndEx: 控件句柄
    :param char: 字符串
    :return: True or Flase
    """
    try:
        for _ in char:
            print('key:%s    ascii:%d'  % (_, ord(_)))
            win32api.PostMessage(hwndEx, win32con.WM_CHAR, ord(_), 0)
            time.sleep(random.uniform(0,0.5))
    except Exception as e:
        print(e)
        return False

    return True
def keyEvent(char):
    try:
        win32api.keybd_event('', 0, 0, 0)
        time.sleep(random.uniform(0, 0.5))
        win32api.keybd_event('', 0, win32con.KEYEVENTF_KEYUP, 0)
    except Exception as e:
        print(e)
    return False
if __name__ == '__main__':
    pass