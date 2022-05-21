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
        self.root.geometry("893x300")
        self.root.title("AUDIOBOOK MAKER")

        current_dir = StringVar()
        current_dir.set(os.getcwd())
        self.file_name = StringVar()

        Entry(self.root,textvariable=current_dir,width=148).place(x=0,y=0)
        Button(self.root,text="SEARCH",height=2,width=10).place(x=10,y=44)
        Entry(self.root,textvariable=self.file_name,width=33,font=('arial',24)).place(x=96,y=44)
        Label(self.root,text="PAGES:").place(x=740,y=53)
        Label(self.root,fg='red',bg='black',height=2,widt=12).place(x=790,y=45)

        self.root.mainloop()

if __name__ == "__main__":
    App()
        
