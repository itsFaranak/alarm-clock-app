
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTimeEdit , QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        # Load the UI file
        uic.loadUi("alarm-clock.ui", self)
        self.setWindowTitle("Alarm Clock")

        # Define our widgets
        # Header
        self.Iconlabel = self.findChild(QLabel, "Iconlabel")
        self.Title_label = self.findChild(QLabel, "Title_label")
        
        # Date & Time 
        self.timeLabel = self.findChild(QLabel, "timeLabel")
        self.dateLabel = self.findChild(QLabel, "dateLabel")
        
        #  Alarm section
        self.selectLabel = self.findChild(QLabel, "selectLabel")
        self.settimeEdit = self.findChild(QTimeEdit, "settimeEdit")
        self.AmPmBox = self.findChild(QComboBox, "AmPmBox")
        self.messageLine = self.findChild(QLineEdit, "messageLine")

        # Buttons
        self.stopButton = self.findChild(QPushButton, "stopButton")
        self.setAlarmButton = self.findChild(QPushButton, "setAlarmButton")
        self.snoozeButton = self.findChild(QPushButton, "snoozeButton")
        
        # Status
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")

         # Alarm variables
        self.alarm_time = None
        self.alarm_message = ""
        self.alarm_active = False
        self.sound = QMediaPlayer()
        self.sound.setMedia(QMediaContent(QUrl.fromLocalFile("Electronic.wav")))
        self.sound.setVolume(100)  # تنظیم حداکثر صدا

        # Create a QTimer that updates the time label every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
        self.update_time()


        # click button signals
        self.setAlarmButton.clicked.connect(self.set_alarm)
        self.stopButton.clicked.connect(self.stop_alarm)
        self.snoozeButton.clicked.connect(self.snooze_alarm)
        self.messageLine.textChanged.connect(self.update_message_display)

       
        # Show the App
        self.show()

    # Get the current time and date
    def update_time(self):
        now = QDateTime.currentDateTime() # گرفتن زمان فعلی
        
        # time
        self.timeLabel.setText(now.toString("HH:mm:ss AP"))
        # date
        self.dateLabel.setText(now.toString("dddd, dd MMM yyyy"))

        # Check alarm
        # Only check alarm if active and set
        if self.alarm_active and self.alarm_time:
            current_time = now.time()
            if current_time.hour() == self.alarm_time.hour() and current_time.minute() == self.alarm_time.minute():
                self.sound.play()
                self.alarm_active = False
                self.lineEdit.setText(f"'Alarm!' {self.alarm_message}")

    def set_alarm(self):
        alarm_time = self.settimeEdit.time() # Alarm time
        self.alarm_message = self.messageLine.text()  # Alarm message
        self.alarm_active = True  # فعال کردن آلارم
        self.lineEdit.setText(f"Alarm set for {alarm_time.toString('hh:mm AP')}")  
        
        #  AM/PM ComboBox
        ampm = self.AmPmBox.currentText()
        if ampm == "PM" and alarm_time.hour() < 12:
            alarm_time = alarm_time.addSecs(12 * 3600)
        elif ampm == "AM" and alarm_time.hour() >= 12:
            alarm_time = alarm_time.addSecs(-12 * 3600)

        self.alarm_time = alarm_time


    def stop_alarm(self):
        self.alarm_active = False  # deactive alarm
        self.lineEdit.setText("Alarm stopped.")
        self.sound.stop() # stop alarm sound

    def snooze_alarm(self):
        if self.alarm_time:
            new_time = self.alarm_time.addSecs(5 * 60)  # Snooze alarm for 5 minutes.
            self.alarm_time = new_time
            self.alarm_active = True
            self.lineEdit.setText(f"Alarm snoozed to {self.alarm_time.toString('hh:mm AP')}")
            self.sound.stop()

    def update_message_display(self, text):
        self.lineEdit.setText(text)

#Initilize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
  
