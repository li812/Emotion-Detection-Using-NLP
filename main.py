#pip install sounddevice --user
#pip install soundfile
#pip install pyaudio
#pip install SpeechRecognition

from tkinter import *
from tkinter import messagebox
import sounddevice
from scipy.io.wavfile import write
import soundfile
from tkinter import filedialog
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import speech_recognition as sr

class main:
    def __init__(self,master):
        self.master=master
        self.duration=StringVar()
        self.fpath=StringVar()
        self.lbl_text=StringVar()

        self.lbl_text.set("waiting")
        master.title("Admin Home")
        master.state("zoomed")
        large_font = ('Verdana', 15)

        lbl_2 = Label(master, text="Duration in Seconds", height=2, width=20, font=large_font).place(x=10, y=10)
        dur = Entry(master,textvariable=self.duration, width=3, font=large_font).place(x=400, y=20)
        sbmitbtn = Button(master, text="RECORD VOICE", height=2, width=20, font=large_font, command=self.recordvoice).place(x=200, y=75)
        lbl = Label(master, text="Select a Voice...", height=2, width=20, font=large_font).place(x=200, y=200)
        voice_emotion = Label(master,textvariable=self.lbl_text, text="Emotion...", height=2, width=20, font=large_font).place(x=900, y=200)
        txt = Entry(master,textvariable=self.fpath, width=20, font=large_font).place(x=200, y=300)
        browse = Button(master, text="Browse", font=large_font, command=self.browsefunc).place(x=700, y=300)
        emotion = Button(master, text="VIEW EMOTION", height=2, width=20, font=large_font, command=self.viewemotion).place(x=200, y=400)
        ext = Button(master, text="Exit", height=2, width=20, font=large_font, command=master.destroy).place(x=200, y=550)
        master.mainloop()

    def recordvoice(self):
        print("record")
        tme = int(self.duration.get().strip())
        print("Time:",tme)
        fs = 44100
        print("Recording.....n")
        record_voice = sounddevice.rec(int(tme * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        write("out.wav", fs, record_voice)
        print("Finished.....nPlease check your ou1tput file")
        data, samplerate = soundfile.read('out.wav')
        soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
        messagebox.showinfo("Record", "Voice recording finished...")
    def browsefunc(self):
        print("browse here")
        try:
            filename = str(filedialog.askopenfilename())
            print("Filepath:",filename)
            self.fpath.set(filename)
        except:
            messagebox.showinfo("Alert", "only wave files supported...")
    def viewemotion(self):
        print("started...")
        path=self.fpath.get().strip()
        print(path)
        r = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text)
                print('Converting audio transcripts into text ...')
                print(text)
                paragraph=text
                lines_list = tokenize.sent_tokenize(paragraph)
                print(lines_list)
                NEG=NEU=POS=0
                for sentence in lines_list:
                    sid = SentimentIntensityAnalyzer()
                    ss = sid.polarity_scores(sentence)
                    k = ss.keys()
                    p = list(k)
                    print("Negative:", ss.get(p[0]), ",Neutral:", ss.get(p[1]), ",Positive:", ss.get(p[2]), ",Sent:",  sentence)
                    NEG=NEG+ss.get(p[0])
                    NEU=NEU+ss.get(p[1])
                    POS=POS+ss.get(p[2])
                if NEG > NEU:
                    if NEG > POS:
                        messagebox.showinfo("Emotion", "Negative Emotion: " + str(NEG))
                    else:
                        messagebox.showinfo("Emotion", "Positive Emotion: " + str(POS))
                else:
                    if NEU>POS:
                        messagebox.showinfo("Emotion", "Neutral Emotion: " + str(NEU))
                    else:
                        messagebox.showinfo("Emotion", "Positive Emotion: " + str(POS))
            except:
                messagebox.showerror("Error", "Sorry, something went wrong. Please try again.")
cp=Tk()
w=main(cp)