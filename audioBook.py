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
        self.ventana.geometry("801x511")
        self.ventana.title("LECTOR DE TEXTOS")
        self.rate=IntVar()
        self.rate.set(130)
        self.text = ""
        self.actv = False
        
        self.resource_manager = PDFResourceManager(caching=True)
        
        self.btnSearch = Button(self.ventana,text="BUSCA PDF",command=lambda:self.init_task(1))
        self.btnSearch.place(x=1,y=7)
        self.btnListen = Button(self.ventana,text="LEER",command=lambda:self.init_task(0))
        self.btnListen.place(x=90,y=7)
        self.label2 = Label(self.ventana,bg='dim gray',fg='white')
        self.label2.pack(side='bottom')        
        self.display=scrolledtext.ScrolledText(self.ventana,background='white',width=97,height=28)
        self.display.pack(side='bottom')
        self.player = pyttsx3.init()
        self.label = Label(self.ventana,text='Speech Rate:',bg='dim gray',fg='white')
        self.label.place(x=150,y=9)
        self.entry = Entry(self.ventana,width=6,textvariable=self.rate)
        self.entry.place(x=227,y=9)
        self.btnSave = Button(self.ventana,text='GUARDA AUDIO',command=lambda:self.init_task(2))
        self.btnSave.place(x=300,y=7)
        self.btnDir = Button(self.ventana,text='SELECT FOLDER',command=self.change_dir)
        self.btnDir.place(x=700,y=7)

        self.ventana.mainloop()

    def change_dir(self):
        direct = filedialog.askdirectory()
        if direct != "":
            os.chdir(direct)
        

    def open(self):
        if self.actv == False:
            file = filedialog.askopenfilename(initialdir="/",title="SELECCIONAR ARCHIVO",
                        filetypes =(("PDF files","*.pdf") ,("all files","*.*")))
            if file != "":
                print(file)
                self.name,ex = os.path.splitext((file.split('/')[-1]))
                try:
                    pages = 0
                    self.display.delete('1.0',END)
                    self.label2.config(text="CARGANDO TEXTO...")
                    out_text = StringIO()
                    codec = 'utf-8'
                    laParams = LAParams()
                    text_converter = TextConverter(self.resource_manager, out_text, laparams=laParams)
                    fp = open(file, 'rb')
                    interpreter = PDFPageInterpreter(self.resource_manager, text_converter)
                    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
                        interpreter.process_page(page)
                        pages += 1
                    self.text = out_text.getvalue()
                    self.correct_speech = self.text.replace('\n',"") 
                    self.label2.config(text='TITULO: {}  ({} Páginas)'.format((file.split('/')[-1]),pages))

                    fp.close()
                    text_converter.close()
                    out_text.close()

                    self.display.insert(END,self.text)
                except:
                    self.label2.config(text="")
                    messagebox.showwarning("ERROR","Se produjo un error al cargar el archivo")
        
                
    def read_text(self):
        if self.text != "" and self.actv==False:
            self.actv = True
            self.player.setProperty('rate',int(self.entry.get()))
            self.player.say(self.correct_speech)
            self.player.runAndWait()
            self.player.stop()
            self.actv = False

    def saveFile(self):
        if self.text != "":
            self.btnSave.config(text="GUARDANDO....")
            try:
                if self.actv == False:
                    self.player.setProperty('rate',int(self.entry.get()))
                    self.player.save_to_file(self.correct_speech,self.name+'.mp3')
                    self.player.runAndWait()
                else:
                    self.tts = gtts.gTTS(self.text,lang='es')
                    self.tts.save(self.name+'.mp3')
                messagebox.showinfo("TAREA COMPLETADA","Archivo creado correctamente")
                self.btnSave.config(text="GUARDA AUDIO")
            except:
                messagebox.showwarning("ERROR","No se pudo completar la acción")

    def init_task(self,i):
        task = [self.read_text,self.open,self.saveFile]
        t = threading.Thread(target=task[i])
        t.start()
            
if __name__=="__main__":
    App()
