#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyttsx3
from tkinter import *
from tkinter import filedialog, messagebox
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
        self.ventana.geometry("1000x599")
        self.ventana.title("AUDIO-TEXT MAKER")
        self.rate=IntVar()
        self.current_dir = StringVar()
        self.current_dir.set(os.getcwd())
        self.rate.set(130)
        self.text = ""
        self.actv = False
        
        self.resource_manager = PDFResourceManager(caching=True)
        
        Entry(self.ventana,textvariable=self.current_dir,bg='light gray',width=166).pack(side=TOP)
        Button(self.ventana,text="SEARCH PDF",command=self.open_file).place(x=9,y=28)
        #self.btnListen = Button(self.ventana,text="LEER")
        #self.btnListen.place(x=90,y=25)
        self.label2 = Label(self.ventana,bg='dim gray',fg='white')
        self.label2.pack(side='bottom')        
        self.display=scrolledtext.ScrolledText(self.ventana,background='white',width=120,height=32)
        self.display.pack(side='bottom')
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
            self.name,ex = os.path.splitext((pdf_file.split('/')[-1]))
            print(self.name)

            
if __name__=="__main__":
    App()
