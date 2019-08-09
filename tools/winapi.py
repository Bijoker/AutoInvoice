import win32gui

def findWindows(hwnd=win32gui.GetDesktopWindow(), classname=None, title=None,mode=0):
    '''

    :param classname:
    :param title:
    :param mode:  0：默认模糊查找， 1：精确查找
    :return:
    '''
    childs = []
    def all_ok(hwnd, param):
        print(hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))
        if mode == 1:
            if win32gui.GetClassName(hwnd) == classname and win32gui.GetWindowText(hwnd) == title:
                print(hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))
                childs.append(hwnd)
        else:
            if win32gui.GetClassName(hwnd) == classname or win32gui.GetWindowText(title) == title:
                print(hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))
                childs.append(hwnd)
        return True
    win32gui.EnumChildWindows(hwnd, all_ok, None)
    return childs


import time
import win32api, win32gui, win32con

hwnd = win32gui.FindWindow(None,'Xshell 6')

def get_child_windows(parent,classname=None, title=None):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd),hwndChildList)
    return hwndChildList
# hwnds = get_child_windows(hwnd, 'Afx:DockPane:960000:8:10005:10')
# print(hwnds)


def all_ok(hwnd, param):
    print(hwnd, win32gui.GetWindowText(hwnd),win32gui.GetClassName(hwnd))
    return True
    # if win32gui.GetClassName(hwnd) == 'NsComboBox':
        # param.append(hwnd)

#     return True
# param = []
# print(win32gui.EnumChildWindows(win32gui.GetDesktopWindow(), all_ok,None))



def findWindows(classname=None, title=None,mode=0):
    '''

    :param classname:
    :param title:
    :param mode:  0：默认模糊查找， 1：精确查找
    :return:
    '''
    childs = []
    hwnd = win32gui.GetDesktopWindow()
    def all_ok(hwnd, param):
        print(hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))
        if mode == 1:
            if win32gui.GetClassName(hwnd) == classname and win32gui.GetWindowText(title) == title:
                print(hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))
                childs.append(hwnd)
        else:
            if win32gui.GetClassName(hwnd) == classname or win32gui.GetWindowText(title) == title:
                print(hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))
                childs.append(hwnd)
        return True
    win32gui.EnumChildWindows(hwnd, all_ok, None)
    return childs



a = findWindows("Afx:ToolBar:960000:8:10005:10")
for i in a:
    print(hex(i))





def find_idxSubHandle(pHandle, winClass, index=0):
    """
    已知子窗口的窗体类名
    寻找第index号个同类型的兄弟窗口
    """
    assert type(index) == int and index >= 0
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)
    while index > 0:
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)
        index -= 1
    return handle


def find_subHandle(pHandle, winClassList):
    """
    递归寻找子窗口的句柄
    pHandle是祖父窗口的句柄
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈
    """
    assert type(winClassList) == list
    if len(winClassList) == 1:
        return find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
    else:
        pHandle = find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
