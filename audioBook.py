import pyttsx3
from tkinter import *
from tkinter import filedialog
#from tkinter.filedialog import *
import tkinter.scrolledtext as scrolledtext
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage


class App:
    def __init__(self):

        self.ventana = Tk()
        self.ventana.configure(bg='dim gray')
        self.ventana.geometry("801x490")
        self.ventana.title("AUDIO BOOK MAKER")
        self.btnSearch = Button(self.ventana,text="BUSCA PDF",command=self.open)
        self.btnSearch.place(x=1,y=7)
        self.display=scrolledtext.ScrolledText(self.ventana,background='white',width=97,height=28)
        self.display.pack(side='bottom')
        #self.display.place(x=2,y=27)

        self.ventana.mainloop()

    def open(self):
        file = filedialog.askopenfilename(initialdir="/",title="SELECCIONAR ARCHIVO",
                    filetypes =(("PDF files","*.pdf") ,("all files","*.*")))
        if file != "":
            pdfreader = PyPDF2.PdfFileReader(file)
            pages = pdfreader.numPages
            self.display.insert(END,'hole')

            resource_manager = PDFResourceManager(caching=True)

            out_text = StringIO()
            
            codec = 'utf-8'
            
            laParams = LAParams()
            
            text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
            fp = open(file, 'rb')
           
            interpreter = PDFPageInterpreter(resource_manager, text_converter)

            for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
                interpreter.process_page(page)

            text = out_text.getvalue()

            fp.close()
            text_converter.close()
            out_text.close()

            self.display.insert(END,text)


if __name__=="__main__":
    App()
