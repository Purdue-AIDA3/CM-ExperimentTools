import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QSizePolicy, QGraphicsView, QStackedLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QFont, QPixmap
import time
from pathlib import Path
from .Task1Clicks import Task1Clicks  # Default clicks class
from Controllers import Task1Controller
import datetime

class Task1(QWidget):

    def __init__(self, file_name, parent=None, audio_files=None, clicks_class=Task1Clicks):
        super().__init__(parent)
        self.setWindowTitle("Task 1")
        self.file_name = file_name
        self.audio_files = audio_files
        self.current_audio_file = 0
        self.clicks_class = clicks_class  # Store the clicks class as an instance variable
        #if audio_files is not None:
        #    file_name += "_secondary"
        self.controller = Task1Controller(file_name)
        self.init_ui()

    def init_ui(self):
        self.media_player = QMediaPlayer()
        self.videoWidget = QVideoWidget()

        controlLayout = QHBoxLayout()
        self.playbutton = QPushButton("Play")
        self.nextButton = QPushButton("Next")
        
        self.playbutton.clicked.connect(self.play_video)
        self.nextButton.clicked.connect(self.next_page)
        self.nextButton.setEnabled(False)

        controlLayout.addWidget(self.playbutton)
        controlLayout.addWidget(self.nextButton)
        self.media_player.setSource(QUrl.fromLocalFile(f"Resources/Task_1/{self.file_name}.mp4"))
        
        if self.audio_files is not None:
            self.timer = QTimer(self)
            self.audio_output = QAudioOutput()
            self.audio_player = QMediaPlayer()
            self.audio_player.setAudioOutput(self.audio_output)
            self.audio_output.setVolume(50)
            self.timer.timeout.connect(self.play_audio)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.videoWidget)
        self.layout.addLayout(controlLayout)

        self.setLayout(self.layout)
        self.media_player.setVideoOutput(self.videoWidget)

    def play_video(self):
        self.media_player.play()
        self.controller.add_start_time()
        self.playbutton.setEnabled(False)
        self.media_player.playbackStateChanged.connect(self.playback_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        if self.audio_files is not None:
            self.timer.start(2000)

    def play_audio(self):
        if self.current_audio_file == len(self.audio_files):
            return
        self.audio_player.setSource(QUrl.fromLocalFile(self.audio_files[self.current_audio_file]))
        self.audio_player.play()
        self.current_audio_file += 1
        self.timer.start(3000)

    def playback_state_changed(self, state):
        if state in {QMediaPlayer.PlaybackState.PausedState, QMediaPlayer.PlaybackState.StoppedState}:
            self.nextButton.setEnabled(True)
            self.controller.add_end_time()
            self.next_page()
    
    def position_changed(self, position):
        if position >= self.media_player.duration() - 60:
            self.media_player.pause()

    def next_page(self):
        pixmap = QPixmap(f"Resources/Task_1/Images/{self.file_name}.png")
        def __thunk(parent):
            # Use the provided clicks_class (either Task1Clicks or Task1ClicksTimer)
            return self.clicks_class(self.file_name, self.videoWidget.width(), self.videoWidget.height(), self.controller, pixmap, parent)
        self.parent().insert_widget((f"Task 1 Clicks for {self.file_name}", __thunk))
