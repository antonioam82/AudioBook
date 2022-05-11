#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyttsx3
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter.scrolledtext as scrolledtext
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
import threading
import gtts
import os

class App:
    def __init__(self):

        self.ventana = Tk()
        self.ventana.configure(bg='dim gray')
        self.ventana.geometry("1061x620")#1000 n630
        self.ventana.title("AUDIO-TEXT MAKER")
        self.rate=IntVar()
        self.current_dir = StringVar()
        self.current_dir.set(os.getcwd())
        self.rate.set(130)
        self.text = ""
        self.actv = False
        
        self.resource_manager = PDFResourceManager(caching=True)
        
        Entry(self.ventana,textvariable=self.current_dir,bg='light gray',width=176).pack(side=TOP)
        Button(self.ventana,text="SEARCH PDF",command=self.init_task).place(x=9,y=28)
        #Button(self.ventana,text="<").pack(side='bottom')
        #Button(self.ventana,text=">").pack(side='right')
        #self.btnListen = Button(self.ventana,text="LEER")
        #self.btnListen.place(x=90,y=25)
        self.pageList = ttk.Combobox(self.ventana,width=12)
        self.pageList.place(x=960,y=29)
        self.label2 = Label(self.ventana,bg='dim gray',fg='white')
        self.label2.pack(side='bottom')        
        self.display=scrolledtext.ScrolledText(self.ventana,background='white',width=128,height=33)#width=120,height=32
        self.display.place(x=9,y=62)
        self.player = pyttsx3.init()
        #self.label = Label(self.ventana,text='Speech Rate:',bg='dim gray',fg='white')
        #self.label.place(x=150,y=30)
        #self.entry = Entry(self.ventana,width=6,textvariable=self.rate)
        #self.entry.place(x=227,y=30)
        #self.btnSave = Button(self.ventana,text='GUARDA AUDIO')
        #self.btnSave.place(x=300,y=25)
        #self.btnDir = Button(self.ventana,text='SELECT FOLDER')
        #self.btnDir.place(x=700,y=25)

        self.ventana.mainloop()

    def open_file(self):
        pdf_file = filedialog.askopenfilename(initialdir="/",title="SELECT FILE",
                        filetypes=(("PDF files","*.pdf"),("all files","*.*")))
        if pdf_file:
            self.pages = 0
            #self.name,ex = os.path.splitext((pdf_file.split('/')[-1]))
            self.name = pdf_file.split('/')[-1]
            out_text = StringIO()
            codec_text = 'utf-8'
            laParams = LAParams()
            text_converter = TextConverter(self.resource_manager, out_text, codec=codec_text, laparams=laParams)
            interpreter = PDFPageInterpreter(self.resource_manager, text_converter)
            with open(pdf_file, 'rb') as fp:
                for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
                    #if pages == 12-1:  #pagina deseada - 1
                    interpreter.process_page(page)
                    self.pages += 1
                    
            self.n_pages()      
            self.text = out_text.getvalue()
            self.display.insert(END, self.text)
            self.text = ""
            
            self.label2.configure(text="TITTLE: {} (PAGES: {})".format(self.name,self.pages))

    def init_task(self):
        t = threading.Thread(target=self.open_file)
        t.start()

    def n_pages(self):
        list_of_pages = []
        for i in range(self.pages):
            list_of_pages.append("PAGE {}".format(i+1))
        self.pageList["values"] = list_of_pages
        self.pageList.set("ALL")

            
if __name__=="__main__":
    App()
