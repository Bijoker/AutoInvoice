import win32con
from win32con import WM_INPUTLANGCHANGEREQUEST
import win32gui
import win32api


def setKeyboardLayout_en(inner):
    '''

    :param inner:
    :return:
    '''
    def wrapper(*args, **kwargs):
        if win32api.LoadKeyboardLayout('0x0409', win32con.KLF_ACTIVATE) == None:
            return Exception('加载键盘失败')
        # 语言代码
        # https://msdn.microsoft.com/en-us/library/cc233982.aspx
        LID = {0x0804: "Chinese (Simplified) (People's Republic of China)",
               0x0409: 'English (United States)'}

        # 获取前景窗口句柄
        hwnd = win32gui.GetForegroundWindow()

        # 获取前景窗口标题
        title = win32gui.GetWindowText(hwnd)
        # 获取键盘布局列表
        im_list = win32api.GetKeyboardLayoutList()
        im_list = list(map(hex, im_list))
        print(im_list)
        oldKey = hex(win32api.GetKeyboardLayout())

        # 设置键盘布局为英文
        result = win32api.SendMessage(
            hwnd,
            WM_INPUTLANGCHANGEREQUEST,
            0,
            0x4090409)
        if result == 0:
            print('设置英文键盘成功！')


        inner(*args,*kwargs)

        result = win32api.SendMessage(
            hwnd,
            WM_INPUTLANGCHANGEREQUEST,
            0,
            oldKey)
        if result == 0:
            print('还原键盘成功！')
    return wrapper


if __name__ == '__main__':
    pass
