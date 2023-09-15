from  tkinter import *

class Application(Frame):

    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.pack()

        self.createWidget()

    def createWidget(self):
        self.btn01=Button(self)
        self.btn01.pack()

root=Tk()
root.geometry("300x300+200+200")
root.title("test")
app=Application(master=root)

root.mainloop()