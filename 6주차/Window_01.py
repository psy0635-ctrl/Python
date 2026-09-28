from tkinter import *

window = Tk()

window.title("윈도창 연습")
# window.geometry("400x100")
window.resizable(width=True, height=True)

label1 = Label(window, text = "파이썬을")
label2 = Label(window, text = "열심히", font = ("궁서체",30), fg = "blue")
label3 = Label(window, text = "공부합시다.", bg = "magenta", width = 100, height = 20 , anchor = SE)

label1.pack()
label2.pack()
label3.pack()

window.mainloop()
