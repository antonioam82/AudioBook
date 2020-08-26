import pyttsx3
import PyPDF2
from tkinter import *
from tkinter.filedialog import *
import tkinter.scrolledtext as scrolledtext

class App:
    def __init__(self):

        self.ventana = Tk()
        self.ventana.configure(bg='dim gray')
        self.ventana.geometry("801x490")
        self.ventana.title("AUDIO BOOK MAKER")
        self.btnSearch = Button(self.ventana,text="BUSCA PDF")
        self.btnSearch.place(x=1,y=7)
        self.display=scrolledtext.ScrolledText(self.ventana,background='white',width=97,height=28)
        self.display.pack(side='bottom')
        #self.display.place(x=2,y=27)

        self.ventana.mainloop()

if __name__=="__main__":
    App()
