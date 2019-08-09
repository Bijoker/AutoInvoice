import win32con,win32gui
def msgBox(hwnd=None, text='提示信息', caption='窗口标题'):
    win32gui.MessageBox(hwnd, text, caption, win32con.MB_OK)
    print(1111111)





if __name__ == '__main__':
    msgBox()