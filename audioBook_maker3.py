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
        self.root.geometry("803x300")
        self.root.title("AUDIOBOOK MAKER")

        current_dir = StringVar()
        current_dir.set(os.getcwd())

        Entry(self.root,textvariable=current_dir,width=133).place(x=0,y=0)

        self.root.mainloop()

if __name__ == "__main__":
    App()
