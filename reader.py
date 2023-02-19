import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer
import gtts
import threading
import shutil
import time



win = Tk()
win.title('READER')
win.geometry('%dx%d' % (win.winfo_screenwidth(), win.winfo_screenheight()))

main_var = StringVar()
but_var = StringVar()
pause_var = StringVar()
prev_list = []


def start_prog():
    try:
        backend.main_work(fetch_content)
        backend.spk()
    except Exception:
        pass


def reading():
    global fetch_content
    try:
        type_of_file = (('text files', '*.txt'), ('All files', '*.*'))
        search_file = filedialog.askopenfilename(filetypes=type_of_file)

        if search_file != '':
            try:
                open_file_but.destroy()
                choose_but = Button(quit_frame, text='CHOOSE ANOTHER FILE', command=reading, font='Consolas 15')
                choose_but.pack(pady=10)
            except Exception:
                pass
        if search_file in os.listdir() is False:
            shutil.copy2(search_file, os.getcwd())
           
        with open(search_file) as file:
            search_file_name = file.name
        try:
            os.rename(search_file_name, 'data.txt')
        except Exception:
            os.remove('data.txt')
            os.rename(search_file_name, 'data.txt')    

        with open('data.txt', 'r', encoding='utf16') as dat:
            fetch_content = dat.read()

        start_prog()
    except Exception as e:
        print(e)


class backend:
    def main_work(self, fetch_content):
        global remaining_content
        self.fetch_content = fetch_content

        with open('reader.log', 'w', encoding='utf16') as log:
            log.write(self.fetch_content)

        if self.fetch_content == '':
            if os.path.exists('reader.log'):
                os.remove('reader.log')

        line_cst = 0
        primary_content = ''
        remaining_content = ''

        self.remaining_content = remaining_content

        for words in self.fetch_content:
            if line_cst < 5:
                primary_content += words
                if words == '।':
                    line_cst += 1
            else:
                self.remaining_content += words

        list_content = primary_content.split()

        addin = 15
        while addin < len(list_content):
            list_content.insert(addin, '\n')
            addin += 15

        main_content = ''
        self.main_content = main_content

        for i in list_content:
            self.main_content += (i + ' ')

        if self.main_content == '':
            main_var.set('Finished!')
            start_but.configure(command=None)

        else:
            main_var.set(self.main_content)

    def previous(self,test =0):
        try:
            prev_content = prev_list[len(prev_list) - 1]
            mixer.init()
            mixer.music.stop()
            mixer.music.unload()
            backend.main_work(prev_content)
            prev_list.pop()
            backend.spk()
        except Exception:
            pass

    def next_fnc(self,test =0):
        try:
            prev_list.append(self.fetch_content)
            mixer.init()
            mixer.music.stop()
            mixer.music.unload()
            backend.main_work(self.remaining_content)
            backend.spk()

        except Exception:
            pass

    def spk(self):
        def thread_spk():
            try:
                start_but.configure(command=None)
                but_var.set('WAIT...')
                tts = gtts.gTTS(self.main_content, lang='hi')
                audio_file = 'bgvoice.mp3'
                tts.save(audio_file)
                but_var.set('START')
                start_but.configure(command=backend.play_file)

            except Exception:
                try:
                    os.remove('bgvoice.mp3')
                    but_var.set('WAIT...')
                    tts = gtts.gTTS(self.main_content, lang='hi')
                    audio_file = 'bgvoice.mp3'
                    tts.save(audio_file)
                    but_var.set('START')
                except Exception:
                    try:
                        but_var.set('START')
                        pass
                    except Exception:
                        pass

        thread_spkin = threading.Thread(target=thread_spk)
        thread_spkin.start()

    def play_file(self,test =0):
        def thread_play_file():
            try:
                mixer.init()
                mixer.music.load('bgvoice.mp3')
                mixer.music.play()
            except Exception:
                try:
                    os.remove('bgvoice.mp3')
                    mixer.init()
                    mixer.music.load('bgvoice.mp3')
                    mixer.music.play()
                except Exception:
                    pass
        try:
            if self.main_content == '':
                start_but.configure(command=None)
            else:
                thread_play = threading.Thread(target=thread_play_file)
                thread_play.start()
        except Exception:
            pass

    def pause(self,test = 0):
        try:
            if mixer.music.get_busy():
                mixer.music.pause()
                pause_var.set('PLAY')

            else:
                mixer.music.unpause()
                pause_var.set('PAUSE')
        except Exception:
            pass

    def quitting(self,sample = 0):
        ask_quit = messagebox.askyesno(title='Confirmation', message='Are you sure that you want to quit?')
        if ask_quit:
            try:
                os.remove('bgvoice.mp3')
                win.destroy()
                quit()
            except Exception:
                try:
                    mixer.music.unload()
                    os.remove("bgvoice.mp3")
                    win.destroy()
                    quit()    
                except Exception:
                    win.destroy()
                    quit()

pause_var.set('PAUSE')

backend = backend()

win.protocol("WM_DELETE_WINDOW", backend.quitting)
win.bind("<space>",backend.pause)
win.bind("<Escape>",backend.quitting)
win.bind("<Right>",backend.next_fnc)
win.bind("<Left>",backend.previous)
win.bind("<s>",backend.play_file)


if os.path.exists('reader.log'):
    ask_load = messagebox.askyesno(title='Reader', message='Do you want to start from where you left?')
    if ask_load:
        with open('reader.log', 'r', encoding='utf16') as log:
            fetch_content = log.read()
        start_prog()
    else:
        try:
            with open('data.txt', 'r', encoding='utf16') as dat:
                fetch_content = dat.read()
            start_prog()
        except Exception:
            main_var.set('FILE NOT FOUND!')
            open_file_but = Button(win, text='CHOOSE FILE', command=reading, font='Consolas 15')
            open_file_but.pack(pady=6)


else:
    try:
        with open('data.txt', 'r', encoding='utf16') as dat:
            fetch_content = dat.read()
        start_prog()
    except Exception:
        main_var.set('FILE NOT FOUND!')
        but_var.set('START')
        open_file_but = Button(win, text='CHOOSE FILE', command=reading, font='Consolas 15')
        open_file_but.pack(pady=6)


show_frame = Frame(win)

show = Label(show_frame, textvar=main_var, font='Consolas 15', fg='Red', bg='white', relief='solid')
show.pack(ipadx=20, pady=50, padx=30)

show_frame.pack()


but_frame = Frame(win)

prev_but = Button(but_frame, text='<PREV', command=backend.previous, font='Consolas 15')
prev_but.pack(side=LEFT, padx=10)

start_but = Button(but_frame, textvar=but_var, command=backend.play_file, font='Consolas 15')
start_but.pack(side=LEFT, padx=10)

next_but = Button(but_frame, text='NEXT>', command=backend.next_fnc, font='Consolas 15')
next_but.pack(padx=10, side=RIGHT)

pause_but = Button(but_frame, textvar=pause_var, command=backend.pause, font='Consolas 15')
pause_but.pack(padx=10)


but_frame.pack(fill=Y)

backend.spk()

quit_frame = Frame(win)

quit_but = Button(quit_frame, text='QUIT', font='Consolas 15', command=backend.quitting)
quit_but.pack(pady=10)

try:
    open_file_but.__class__ is None
except Exception:
    choose_but = Button(quit_frame, text='CHOOSE ANOTHER FILE', command=reading, font='Consolas 15')
    choose_but.pack(pady=10)

quit_frame.pack(fill=Y)


win.mainloop()
