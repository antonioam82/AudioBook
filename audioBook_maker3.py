#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyttsx3
import PyPDF2
from tkinter import filedialog, messagebox, ttk, Tk

from googletrans import Translator
import threading
import os

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x300")
        self.root.title("AUDIOBOOK MAKER")

        self.root.mainloop()

if __name__ == "__main__":
    App()
