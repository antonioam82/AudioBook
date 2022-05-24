#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyttsx3
import PyPDF2
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from googletrans import Translator
import threading
import os

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("893x215")
        self.root.title("AUDIOBOOK MAKER")

        current_dir = StringVar()
        current_dir.set(os.getcwd())
        self.file_name = StringVar()

        Entry(self.root,textvariable=current_dir,width=148).place(x=0,y=0)
        Button(self.root,text="SEARCH",height=2,width=11,bg='gray78',command=self.open_file).place(x=10,y=44)
        Entry(self.root,textvariable=self.file_name,width=33,font=('arial',24)).place(x=98,y=44)
        Label(self.root,text="PAGES:").place(x=740,y=53)
        Label(self.root,width=97).place(x=11,y=93)
        self.pages_label = Label(self.root,fg='red',bg='black',width=8,font=("arial",15))
        self.pages_label.place(x=790,y=48)
        Label(self.root,text="LANG:").place(x=740,y=128)
        self.lang_label = Label(self.root,fg='red',bg='black',width=8,font=("arial",15))
        self.lang_label.place(x=790,y=124)
        Button(self.root,text="CREATE AUDIO-BOOK",height=2,width=97,bg='gray78').place(x=10,y=121)
        

        self.root.mainloop()

    def open_file(self):
        try:
            self.pdf_file = filedialog.askopenfilename(initialdir="/",title="SELECT FILE",
                                    filetypes=(("PDF files","*.pdf"),("all files","*.*")))
            if self.pdf_file:
                self.file_name.set(self.pdf_file.split('/')[-1])
                with open(self.pdf_file, 'rb') as book:
                    reader = PyPDF2.PdfFileReader(book)
                    pages = reader.numPages
                self.pages_label.configure(text=pages)
                
        except Exception as e:
            messagebox.showwarning("LOAD ERROR",str(e))

if __name__ == "__main__":
    App()
        
        
        
