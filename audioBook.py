import pyttsx3
import PyPDF2
from tkinter import *
from tkinter.filedialog import *

class App:
    def __init__(self):

        self.ventana = Tk()
        self.ventana.geometry("800x500")
        self.ventana.title("AUDIO BOOK MAKER")

        self.ventana.mainloop()

if __name__=="__main__":
    App()
