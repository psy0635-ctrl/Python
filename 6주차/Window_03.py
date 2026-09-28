from tkinter import *
from tkinter import messagebox

def myFunc():
    messagebox.showinfo("강아지 버튼","강아지가 보입니다.")

window = Tk()

window.title("윈도창 연습")


photo = PhotoImage(file="C:/study/Python/6주차/GIF/dog2.gif")

button = Button(window, image = photo, command = myFunc)
button.pack()


window.mainloop()


