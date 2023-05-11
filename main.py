#pip install sounddevice --user
#pip install soundfile
#pip install pyaudio
#pip install SpeechRecognition

import sys
import sounddevice
from scipy.io.wavfile import write
import soundfile
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets, QtCore
import sounddevice
import soundfile
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import speech_recognition as sr

class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.duration = QLineEdit(self)
        self.fpath = QLineEdit(self)
        self.lbl_text = QLabel(self)


        self.initUI()

    def initUI(self):
        self.setWindowTitle("Emotion-Detection-Using-NLP")
        self.setGeometry(100, 100, 290, 525)
        large_font = QFont('Verdana', 15)

        lbl_2 = QLabel("Duration in Seconds   ", self)
        lbl_2.move(20, 20)
        lbl_2.resize(250, 50)

        self.duration = QLineEdit(self)
        self.duration.move(150, 20)
        self.duration.resize(50, 50)
        self.duration.setText("")

        sbmitbtn = QPushButton("RECORD VOICE", self)
        sbmitbtn.move(20, 100)
        sbmitbtn.resize(250, 50)
        sbmitbtn.setFont(large_font)
        sbmitbtn.clicked.connect(self.recordvoice)

        lbl = QLabel("Select a Voice...", self)
        lbl.move(20, 150)
        lbl.resize(250, 50)

        self.fpath = QLineEdit(self)
        self.fpath.move(20, 200)
        self.fpath.resize(250, 50)

        browse = QPushButton("Browse", self)
        browse.move(20, 250)
        browse.resize(250, 50)
        browse.setFont(large_font)
        browse.clicked.connect(self.browsefunc)

        emotion = QPushButton("VIEW EMOTION", self)
        emotion.move(20, 350)
        emotion.resize(250, 50)
        emotion.setFont(large_font)
        emotion.clicked.connect(self.viewemotion)

        ext = QPushButton("Exit", self)
        ext.move(20, 450)
        ext.resize(250, 50)
        ext.setFont(large_font)
        ext.clicked.connect(self.close)




    def recordvoice(self):
        print("record")
        duration_value = self.duration.text().strip()
        if duration_value:
            tme = int(duration_value)
        else:
            # handle the case where the duration field is empty
            tme = 0 # for example, set the duration to 0 seconds


        print("Time:",tme)
        fs = 44100
        #second = int(input("Enter time duration in seconds: "))
        print("Recording.....n")
        #record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
        record_voice = sounddevice.rec(int(tme * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        write("out.wav", fs, record_voice)
        print("Finished.....nPlease check your ou1tput file")
        data, samplerate = soundfile.read('out.wav')
        soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
        QMessageBox.information(self, "Record", "Voice recording finished...")

    def browsefunc(self):
        print("browse here")
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Wave Files (*.wav)")
            print("Filepath:", filename)
            self.fpath.setText(filename)
        except:
            QMessageBox.information(self, "Alert", "only wave files supported...")

    def viewemotion(self):
        print("started...")
        path=self.fpath.text().strip()
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
                        QMessageBox.information(self, "Emotion", "Negative Emotion: " + str(NEG))
                    else:
                        QMessageBox.information(self, "Emotion", "Positive Emotion: " + str(POS))
                else:
                    if NEU>POS:
                        QMessageBox.information(self, "Emotion", "Neutral Emotion: " + str(NEU))
                    else:
                        QMessageBox.information(self, "Emotion", "Positive Emotion: " + str(POS))
            except:
                QMessageBox.critical(self, "Error", "Sorry, something went wrong. Please try again.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
