from tkinter import *
from Crowler import getText
root = Tk()

text = getText()
print(text)
w2 = Label(root,
           justify=LEFT,
           padx = 10,
           text=text).pack(side="left")
root.mainloop()
