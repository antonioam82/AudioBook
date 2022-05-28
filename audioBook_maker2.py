#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter.scrolledtext as scrolledtext
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from googletrans import Translator
from pdfminer.pdfpage import PDFPage
import threading
from gtts import gTTS
import os

LANGUAGES = {'af': 'afrikaans','sq': 'albanian','am': 'amharic','ar': 'arabic','hy': 'armenian',
'az': 'azerbaijani','eu': 'basque','be': 'belarusian','bn': 'bengali','bs': 'bosnian','bg': 'bulgarian',
'ca': 'catalan','ceb': 'cebuano','ny': 'chichewa','zh-cn': 'chinese (simplified)','zh-tw': 'chinese (traditional)',
'co': 'corsican','hr': 'croatian','cs': 'czech','da': 'danish','nl': 'dutch','en': 'english','eo': 'esperanto',
'et': 'estonian','tl': 'filipino','fi': 'finnish','fr': 'french','fy': 'frisian','gl': 'galician','ka': 'georgian',
'de': 'german','el': 'greek','gu': 'gujarati','ht': 'haitian creole','ha': 'hausa','haw': 'hawaiian','iw': 'hebrew',
'he': 'hebrew','hi': 'hindi','hmn': 'hmong','hu': 'hungarian','is': 'icelandic','ig': 'igbo','id': 'indonesian',
'ga': 'irish','it': 'italian','ja': 'japanese','jw': 'javanese','kn': 'kannada','kk': 'kazakh','km': 'khmer',
'ko': 'korean','ku': 'kurdish (kurmanji)','ky': 'kyrgyz','lo': 'lao','la': 'latin','lv': 'latvian','lt': 'lithuanian',
'lb': 'luxembourgish','mk': 'macedonian','mg': 'malagasy','ms': 'malay','ml': 'malayalam','mt': 'maltese','mi': 'maori',
'mr': 'marathi','mn': 'mongolian','my': 'myanmar (burmese)','ne': 'nepali','no': 'norwegian','or': 'odia','ps': 'pashto',
'fa': 'persian','pl': 'polish','pt': 'portuguese','pa': 'punjabi','ro': 'romanian','ru': 'russian','sm': 'samoan',
'gd': 'scots gaelic','sr': 'serbian','st': 'sesotho','sn': 'shona','sd': 'sindhi','si': 'sinhala','sk': 'slovak',
'sl': 'slovenian','so': 'somali','es': 'spanish','su': 'sundanese','sw': 'swahili','sv': 'swedish','tg': 'tajik',
'ta': 'tamil','te': 'telugu','th': 'thai','tr': 'turkish','uk': 'ukrainian','ur': 'urdu','ug': 'uyghur','uz': 'uzbek',
'vi': 'vietnamese','cy': 'welsh','xh': 'xhosa','yi': 'yiddish','yo': 'yoruba','zu': 'zulu'}


class App:
    def __init__(self):

        self.ventana = Tk()
        self.ventana.configure(bg='dim gray')
        self.ventana.geometry("1061x624")#1000 n630
        self.ventana.title("PDF-AUDIO-TEXT MAKER")
        self.translator = Translator()
        self.loaded = ""
        #self.rate=IntVar()
        self.current_dir = StringVar()
        self.current_dir.set(os.getcwd())
        #self.rate.set(130)
        self.doc = StringVar()
        self.text = ""
        #self.actv = False
        
        self.resource_manager = PDFResourceManager(caching=True)
        
        Entry(self.ventana,textvariable=self.current_dir,bg='light gray',width=176).place(x=0,y=0)#.pack(side=TOP)
        Button(self.ventana,text="SEARCH PDF",command=self.init_task).place(x=9,y=28)
        Entry(self.ventana,textvariable=self.doc,width=13,font=("arial",14)).place(x=90,y=27)
        Button(self.ventana,text="GO",command=self.go_to_page).place(x=1028,y=30)
        Button(self.ventana,text="SAVE AUDIOBOOK",command=self.init_task2).place(x=260,y=28)
        Label(self.ventana,text="LANG:",bg="dim gray",fg="white").place(x=730,y=29)
        self.langList = ttk.Combobox(self.ventana,width=12)
        self.langList.place(x=769,y=29)
        Button(self.ventana,text="<",command=lambda:self.move(-1)).place(x=9,y=597)
        Button(self.ventana,text=">",command=lambda:self.move(1)).place(x=1036,y=597)
        #self.btnListen = Button(self.ventana,text="LEER")
        #self.btnListen.place(x=90,y=25)
        Label(self.ventana,text="PAGES:",bg="dim gray",fg="white").place(x=888,y=29)
        self.pageList = ttk.Combobox(self.ventana,width=12)
        self.pageList.place(x=931,y=29)
        self.label2 = Label(self.ventana,bg='dim gray',fg='white',width=143)
        self.label2.place(x=28,y=599)
        #self.label2.pack(side='bottom')        
        self.display=scrolledtext.ScrolledText(self.ventana,background='white',width=128,height=33)#width=120,height=32
        self.display.place(x=9,y=62)
        #self.player = pyttsx3.init()

        self.keys = list(LANGUAGES.keys())
        self.langList["values"] = list(LANGUAGES.values())
        self.langList.set("english")

        self.ventana.mainloop()

    def open_file(self):
        try:
            self.display.config(state=NORMAL)
            self.pdf_file = filedialog.askopenfilename(initialdir="/",title="SELECT FILE",
                                    filetypes=(("PDF files","*.pdf"),("all files","*.*")))
            if self.pdf_file:
                self.loaded = self.pdf_file
                self.pages = 0
                #self.name,ex = os.path.splitext((pdf_file.split('/')[-1]))
                self.name = self.pdf_file.split('/')[-1]
                self.out_text = StringIO()
                self.codec_text = 'utf-8'
                self.laParams = LAParams()
                self.text_converter = TextConverter(self.resource_manager, self.out_text, codec=self.codec_text, laparams=self.laParams)
                self.interpreter = PDFPageInterpreter(self.resource_manager, self.text_converter)
                
                self.label2.configure(text="LOADING TEXT...")
                with open(self.pdf_file, 'rb') as fp:
                    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
                        self.interpreter.process_page(page)
                        self.pages += 1
                    
                self.n_pages()      
                self.text = self.BMP(self.out_text.getvalue())
                self.lang = (self.translator.translate(self.text).src)
                print(self.lang)
                self.langList.set(LANGUAGES[self.lang])
                self.display.delete('1.0', END)
                self.display.insert(END, self.text)
                self.display.config(state=DISABLED)##
            
                self.label2.configure(text="TITTLE: {} (PAGES: {})".format(self.name,self.pages))
                self.doc.set(self.name)
            else:
                if self.loaded != "":
                    self.pdf_file = self.loaded
                
        except Exception as e:
            messagebox.showwarning("LOAD ERROR", str(e))
            self.label2.configure(text="")

    def BMP(self,s):
        return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))
        

    def go_to_page(self):
        if self.text != "":
            self.display.config(state=NORMAL)
            pages = 0
            self.display.delete('1.0', END)
            self.out_text = StringIO()
            self.text_converter = TextConverter(self.resource_manager, self.out_text, codec=self.codec_text, laparams=self.laParams)
            self.interpreter = PDFPageInterpreter(self.resource_manager, self.text_converter)
            with open(self.pdf_file, 'rb') as fp:
                for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
                    if self.pageList.get() == "ALL PAGES":
                        self.interpreter.process_page(page)
                    else:
                        if pages == int(self.pageList.get().split(' ')[-1])-1:
                            print(pages)
                            self.interpreter.process_page(page)
                            break
                    pages+=1
                    
            self.text = self.BMP(self.out_text.getvalue())
            if self.pageList.get() != "ALL PAGES":
                self.display.insert(END, "*"*60+"PAGE: {}".format(pages+1)+"*"*60+"\n")
            self.display.insert(END, self.text)
            self.display.config(state=DISABLED)##

    def init_task(self):
        t = threading.Thread(target=self.open_file)
        t.start()

    def n_pages(self):
        self.list_of_pages = []
        for i in range(self.pages):
            self.list_of_pages.append("PAGE {}".format(i+1))
        self.list_of_pages.append("ALL PAGES")
        self.pageList["values"] = self.list_of_pages
        self.pageList.set("ALL PAGES")#("ALL PAGES")

    def move(self,mov):
        if self.text != "":
            current_pos = self.list_of_pages.index(self.pageList.get())
            if current_pos + 1 == len(self.list_of_pages):
                current_pos = -1
            self.pageList.set(self.list_of_pages[current_pos+(mov)])
            
            self.go_to_page()
            print(current_pos)

    def init_task2(self):
        if self.text != "": 
            t = threading.Thread(target=self.create_audio_file)
            t.start()
        else:
            messagebox.showwarning("NO INFO","No text to convert.")

    def create_audio_file(self):
        audio_book = filedialog.asksaveasfilename(initialdir="/",title="Save as",defaultextension=".mp3")
        if audio_book:
            self.label2.configure(text="SAVING: {}".format(audio_book.split('/')[-1]))
            try:
                chosen_lan = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.langList.get())]
                tts = gTTS(self.text,lang=chosen_lan)################
                tts.save(audio_book)
                self.label2.configure(text="TITTLE: {} (PAGES: {})".format(self.name,self.pages))
                messagebox.showinfo("SAVED","Saved file '{}'".format(audio_book.split('/')[-1]))
            except Exception as e:
                messagebox.showwarning("UNEXPECTED ERROR",str(e))
            
if __name__=="__main__":
    App()
