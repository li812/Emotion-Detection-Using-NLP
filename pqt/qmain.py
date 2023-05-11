#pip install sounddevice --user
#pip install soundfile
#pip install pyaudio
#pip install SpeechRecognition

import sys
import sounddevice
from scipy.io.wavfile import write
import soundfile
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import speech_recognition as sr

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.duration = QLineEdit(self)
        self.fpath = QLineEdit(self)
        self.lbl_text = QLabel(self)
        self.lbl_text.setText("waiting")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Admin Home")
        self.setGeometry(100, 100, 1200, 700)
        large_font = ('Verdana', 15)

        lbl_2 = QLabel("Duration in Seconds", self)
        lbl_2.move(10, 10)
        lbl_2.resize(250, 50)
        self.duration.move(400, 20)
        self.duration.resize(50, 50)

        sbmitbtn = QPushButton("RECORD VOICE", self)
        sbmitbtn.move(200, 75)
        sbmitbtn.resize(250, 50)
        sbmitbtn.setFont(large_font)
        sbmitbtn.clicked.connect(self.recordvoice)

        lbl = QLabel("Select a Voice...", self)
        lbl.move(200, 200)
        lbl.resize(250, 50)
        self.lbl_text.move(900, 200)
        self.lbl_text.resize(250, 50)

        txt = QLineEdit(self)
        txt.move(200, 300)
        txt.resize(250, 50)
        txt.setText("")
        self.fpath.move(200, 300)
        self.fpath.resize(250, 50)

        browse = QPushButton("Browse", self)
        browse.move(700, 300)
        browse.resize(250, 50)
        browse.setFont(large_font)
        browse.clicked.connect(self.browsefunc)

        emotion = QPushButton("VIEW EMOTION", self)
        emotion.move(200, 400)
        emotion.resize(250, 50)
        emotion.setFont(large_font)
        emotion.clicked.connect(self.viewemotion)

        ext = QPushButton("Exit", self)
        ext.move(200, 550)
        ext.resize(250, 50)
        ext.setFont(large_font)
        ext.clicked.connect(self.close)

    def recordvoice(self):
        print("record")
        tme = int(self.duration.text().strip())
        print("Time:", tme)
        fs = 44100
        print("Recording.....n")
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
            print("Emotion....")
            try:
                filename = self.fpath.text().strip()
                if filename:
                    r = sr.Recognizer()
                    with sr.AudioFile(filename) as source:
                        audio_text = r.record(source)
                        text = r.recognize_google(audio_text)
                    print("Text:", text)
                    sid = SentimentIntensityAnalyzer()
                    sentences = tokenize.sent_tokenize(text)
                    for sentence in sentences:
                        scores = sid.polarity_scores(sentence)
                        for key in sorted(scores):
                            print('{0}: {1}, '.format(key, scores[key]), end='')
                        print()
                else:
                    QMessageBox.information(self, "Alert", "Please select a voice file to view emotion...")
            except:
                QMessageBox.information(self, "Alert", "Error occured while performing operation...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
