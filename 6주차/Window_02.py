from tkinter import *

window = Tk()

window.title("윈도창 연습")
# window.geometry("400x100")
window.resizable(width=True, height=True)

photo1 = PhotoImage(file="C:/study/Python/6주차/GIF/dog.gif")
photo2 = PhotoImage(file="C:/study/Python/6주차/GIF/dog2.gif")
photo3 = PhotoImage(file="C:/study/Python/6주차/GIF/dog3.gif")

label1 = Label(window, image = photo1)
label2 = Label(window, image = photo2)
label3 = Label(window, image = photo3)

label1.pack()
label2.pack()
label3.pack()

window.mainloop()


