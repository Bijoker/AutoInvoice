# coding: UTF-8
# RequireAdmin
import os
import sys
import time
import win32security
from ctypes import *



print(os.getpid())
# if windll.shell32.IsUserAnAdmin():
#     pass
# else:
#     # Re-run the program with admin rights
#     windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)


def requireAdministrator(f):
    def inner(*args, **kwargs):
        if windll.shell32.IsUserAnAdmin():
            f()
        else:
            # Re-run the program with admin rights
            windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
            f()
        return f
    return inner


# def requireAdministrator():
#     if windll.shell32.IsUserAnAdmin():
#         pass
#     else:
#         # Re-run the program with admin rights
#         windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)



def test():
    flags = win32security.TOKEN_ADJUST_PRIVILEGES
    print(flags)
    a = windll.shell32.IsUserAnAdmin()
    print(a)
    # user32 = windll.LoadLibrary("C:\\Windows\\System32\\user32.dll")
    windll.user32.BlockInput(True)
    time.sleep(5)
    windll.user32.BlockInput(False)


    time.sleep(2)

if __name__ == '__main__':
    test()