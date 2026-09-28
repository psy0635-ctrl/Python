from tkinter import *
from tkinter import messagebox

def myFunc():
    if chk.get() == 0:
        messagebox.showinfo("", "체크버튼이 꺼졌습니다.")
    else:
        messagebox.showinfo("", "체크버튼이 켜졌습니다.")
        

window = Tk()

window.title("윈도창 연습")

chk = IntVar()

ckb = Checkbutton(window, text = "클릭해보세요", variable = chk , command = myFunc)
ckb.pack()


window.mainloop()
