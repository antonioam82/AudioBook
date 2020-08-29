import pyttsx3
from tkinter import *
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
import threading

class App:
    def __init__(self):

        self.ventana = Tk()
        self.ventana.configure(bg='dim gray')
        self.ventana.geometry("801x490")
        self.ventana.title("LECTOR PDFs")
        self.rate=IntVar()
        self.rate.set(130)
        self.text = ""
        
        self.resource_manager = PDFResourceManager(caching=True)
        
        self.btnSearch = Button(self.ventana,text="BUSCA PDF",command=self.init_open)
        self.btnSearch.place(x=1,y=7)
        self.btnListen = Button(self.ventana,text="LEER",command=self.initRead)
        self.btnListen.place(x=90,y=7)
        self.display=scrolledtext.ScrolledText(self.ventana,background='white',width=97,height=28)
        self.display.pack(side='bottom')
        self.player = pyttsx3.init()
        self.label = Label(self.ventana,text='Speech Rate:',bg='dim gray',fg='white')
        self.label.place(x=150,y=9)
        self.entry = Entry(self.ventana,width=6,textvariable=self.rate)
        self.entry.place(x=227,y=9)

        self.ventana.mainloop()

    def open(self):
        file = filedialog.askopenfilename(initialdir="/",title="SELECCIONAR ARCHIVO",
                    filetypes =(("PDF files","*.pdf") ,("all files","*.*")))
        if file != "":
            self.display.delete('1.0',END)
            out_text = StringIO()
            codec = 'utf-8'
            laParams = LAParams()
            text_converter = TextConverter(self.resource_manager, out_text, laparams=laParams)
            fp = open(file, 'rb')
            interpreter = PDFPageInterpreter(self.resource_manager, text_converter)
            for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
                interpreter.process_page(page)

            self.text = out_text.getvalue()

            fp.close()
            text_converter.close()
            out_text.close()

            self.display.insert(END,self.text)
        

    def read_text(self):
        self.player.setProperty('rate',int(self.entry.get()))
            
        self.player.say(self.text)
        self.player.runAndWait()
        self.player.stop()

    def initRead(self):
        t = threading.Thread(target=self.read_text)
        t.start()

    def init_open(self):
        t0 = threading.Thread(target=self.open)
        t0.start()
            
if __name__=="__main__":
    App()
