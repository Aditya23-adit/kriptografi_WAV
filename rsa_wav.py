from tkinter import *
import tkinter.font
import scipy.io.wavfile
import numpy as np
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import sys
import wave
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog
import random

global info_channel

def enkrip() : 
    start = time.time()
    file = filename
    hasil_file = StringVar()
    hasil_file = file
    e = input_E.get() 
    n = input_N.get()
    
    e = int(e)
    n = int(n)
    
    if(channels==2 ) :
        fs, audio = scipy.io.wavfile.read(file)
        print(audio)
        audio = audio.astype(np.int16)
        print(audio)
        a, b = audio.shape
        tup = (a, b)
        data = audio
        data.setflags(write=1)
        Time= np.linspace(0, len(data)/fs, num=len(data))
        print(type(Time))
        plt.figure(1)
        plt.title('Original'+ hasil_file)
        plt.plot(Time, data) 
        plt.savefig('Original.png')
        for i in range(0, tup[0]) :
            z = i+1 
            for j in range (tup[1]) :
                x = int(data[i][j])
                if(data[i][j] >= 0) :
                    y = pow(x,e,n)
                    if(y == 0) :
                        data[i][j] = x
                    else :
                        data[i][j] = y
                else : 
                    data[i][j] = x
        
        print("looping selesai")
        enkrip = data.copy()
        enkrip.setflags(write=1)
        enkrip=enkrip.astype(np.int16)
        Time= np.linspace(0, len(enkrip)/fs, num=len(enkrip))
        print(type(Time))
        plt.figure(2)
        plt.title('enkrip'+ hasil_file)
        plt.plot(Time, enkrip) 
        plt.savefig('enkrip.png')
        print(enkrip)     
        scipy.io.wavfile.write('Enkrip.wav', fs, enkrip)
    else : 
        binarySound = {}
        binaryHeader = {}
        song = {}
        with open(file,'rb') as f:
            dt = np.dtype(int)
            dt = dt.newbyteorder('>')
            buffer = f.read(44)
            binaryHeader = np.frombuffer(buffer,dtype=np.int16) #TODO remove the file header 
            buffer = f.read()
            binarySound = np.frombuffer(buffer,dtype=np.int16)
        fs = FS
        data = binarySound.copy()
        for i in range(len(data)) :
            if(data[i]>0) :  
                x = int(data[i])
                x = pow(x,e,n)
                data[i] = x
        enkrip = data.copy()
        enkrip = enkrip.astype(np.int16)
        Time= np.linspace(0, len(enkrip)/fs, num=len(enkrip))
        print(type(Time))
        plt.figure(2)
        plt.plot(Time, data) 
        plt.savefig('enkrip.png')
        plt.title('enkrip'+ hasil_file)        
        scipy.io.wavfile.write('Enkrip.wav', fs, enkrip)
    
    end = time.time()
    endTime = (end-start)
    print(endTime)
    varTime.set(endTime)
    
    pass
   
def dekrip() :
    file = filename
    hasil_file = StringVar()
    hasil_file = filename
    
    n = input_N.get()
    d = input_D.get()
    
    n = int(n)
    d = int(d)
    
    start = time.time()
    if(channels==2 ) :
        fs, audio = scipy.io.wavfile.read(file)
        audio = audio.astype(np.int16)
        a, b = audio.shape
        tup = (a, b)
        dekrip = audio
        dekrip.setflags(write=1)
        for i in range(len(dekrip)) : 
            for j in range (tup[1]) :
                if(dekrip[i][j] > 0) : 
                    x = int(dekrip[i][j])
                    y = pow(x,d,n)
                    dekrip[i][j] = y
        
        print(type(dekrip))
        dekrip = np.array(dekrip)
        dekrip = dekrip.astype(np.int16)
        Time= np.linspace(0, len(dekrip)/fs, num=len(dekrip))
        print(type(Time))
        plt.figure(3)
        plt.plot(Time, dekrip) 
        plt.savefig('dekrip.png')
        plt.title('dekrip'+ hasil_file)
        scipy.io.wavfile.write('Dekrip.wav', fs, dekrip) 
    
    else :
        binarySound = {}
        binaryHeader = {}
        song = {}
        with open(file,'rb') as f:
            dt = np.dtype(int)
            dt = dt.newbyteorder('>')
            buffer = f.read(44)
            binaryHeader = np.frombuffer(buffer,dtype=np.int16) #TODO remove the file header 
            buffer = f.read()
            binarySound = np.frombuffer(buffer,dtype=np.int16)
        fs = FS
        data = binarySound.copy()
        for i in range(len(data)) :
            if(data[i]>0) :  
                x = int(data[i])
                x = pow(x,d,n)
                data[i] = x
        
        dekrip = data.copy()
        dekrip = np.array(dekrip)
        dekrip = dekrip.astype(np.int16)
        Time= np.linspace(0, len(dekrip)/fs, num=len(dekrip))
        print(type(Time))
        plt.figure(2)
        plt.title('dekrip'+ hasil_file)
        plt.plot(Time, dekrip) 
        plt.savefig('dekrip.png')        
        scipy.io.wavfile.write('Dekrip.wav', fs, dekrip)
        
    end = time.time()
    endTime = (end-start)
    print(endTime)
    varTime.set(endTime)
    pass    

def load_file():
    global filename
    global channels
    global FS
    start = time.time()
    filename = askopenfilename()
    foo = wave.open(filename, 'rb')
    channels = foo.getnchannels()
    FS = foo.getframerate()
    
    e1.configure(text = filename)
    varChannel.set(channels)
    varFramerate.set(FS)


#display
root = Tk()
root.geometry("600x300")
changefont = tkinter.font.Font(size=20)
varChannel = StringVar()
varFramerate = StringVar()
varTime = StringVar()

#bgd = PhotoImage(file = "C:\\Users\\USER\\Desktop\\skripsi\\program\\bg.png")
#canvas1 = Canvas(root, width = 600, height = 300)
#canvas1.pack(fill = "both", expand = True)
 
#canvas1.create_image(0, 0, image = bgd, anchor ="nw")
### ENKRIP
judul_enkrip = Label(root,text = "ENKRIP RSA",font =changefont)
judul_enkrip.place(x =20,y = 10)


labelfr = LabelFrame(root,text = "result",padx=20,pady=20)
labelfr.place(x = 60,y = 380)


nilai_d = Label(root,text = "Masukkan Nilai D").place(x = 20, y =100)
nilai_e = Label(root,text = "Masukkan Nilai E").place(x = 20, y =140)
nilai_n = Label(root,text = "Masukkan Nilai N").place(x = 20, y =180)

e1 = Label(root,width=35, text = "", borderwidth = 1, relief = "groove")
e1.place(x = 20, y = 80)

input_D = Entry(root,width=40)
input_E = Entry(root,width=40)
input_N = Entry(root,width=40)

input_D.place(x = 20, y = 120)
input_E.place(x = 20, y = 160)
input_N.place(x = 20, y = 200)


btn_enkrip 	    = Button(root,text = "Enkrip",command=enkrip).place(x = 100,y = 230)
btn_dekrip 	    = Button(root,text = "Dekrip",command=dekrip).place(x = 150,y = 230)
btn_LoadFile 	= Button(root,text = "Pilih File",command=load_file).place(x = 20,y = 50)

### DEKRIP
info_audio = Label(root,text = "INFO AUDIO",font =changefont)
info_audio.place(x =300,y = 10)

channel     = Label(root,text = "channels               : ").place(x=300, y=80)
framerate   = Label(root,text = "framerate              : ").place(x=300, y=120)
waktu       = Label(root,text = "time (second)      : ").place(x=300, y=160)

channel_info    = Label(root,text = "channels", textvariable = varChannel, width=10, borderwidth=1, relief="groove").place(x=400, y=80)
framerate_info  = Label(root,textvariable = varFramerate, width=10, borderwidth=1, relief="groove").place(x=400, y=120)
time_info       = Label(root,textvariable = varTime).place(x=400, y=160)
root.mainloop()