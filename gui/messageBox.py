from tkinter import *
from tkinter.messagebox import *


class MessageBox:
    def __init__(self, title='提示', geometry='200x100+500-100', resizable=False, *args, **kwargs):
        """
        自定义确认取消框
        :param title:
        :param geometry:
        :param resizable:
        :param args:
        :param kwargs:
        :return MyDialog.e   True or False
        """
        self.e = None
        self.win = Tk()
        self.win.title(title)
        self.win.geometry(geometry)
        self.win.resizable(width=resizable, height=resizable)

        l = Label(self.win, text="信息无误请审核\n 错误请跳过", font=("Arial", 12))
        l.pack(side=TOP)

        frm = Frame(self.win, borderwidth=10)
        frm2 = Frame(frm)

        b1 = Button(frm2, text='跳过', command=self.step, borderwidth=2).pack(side=LEFT)
        b2 = Button(frm2, text='审核', command=self.audit, borderwidth=2).pack(side=RIGHT)
        frm2.pack()
        frm.pack()
        self.win.mainloop()
    def step(self):
        self.win.destroy()
        self.win.quit()
        self.e = False
    def audit(self):
        self.win.destroy()
        self.win.quit()
        self.e = True
