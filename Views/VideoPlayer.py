import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QSizePolicy
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont

class VideoPlayer(QWidget):

    def __init__(self, title, file, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.init_ui(title, file)

    def init_ui(self, title, file):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(50)

        videoWidget = QVideoWidget()

        layout = QVBoxLayout()
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setFixedHeight(50)
        layout.addWidget(title_label)
        layout.addWidget(videoWidget)

        controlLayout = QHBoxLayout()
        self.pauseButton = QPushButton("Play")
        self.replayButton = QPushButton("Replay")
        self.nextButton = QPushButton("Next")
        self.nextButton.setEnabled(False)
        
        self.pauseButton.clicked.connect(self.pause_video)
        self.replayButton.clicked.connect(self.replay_video)
        self.nextButton.clicked.connect(self.next_page)

        controlLayout.addWidget(self.pauseButton)
        controlLayout.addWidget(self.replayButton)
        controlLayout.addWidget(self.nextButton)
        
        layout.addLayout(controlLayout)

        self.setLayout(layout)

        self.media_player.setVideoOutput(videoWidget)
        self.media_player.setSource(QUrl.fromLocalFile(file))
        self.media_player.playbackStateChanged.connect(self.playback_state_changed)

    def pause_video(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.pauseButton.setText("Play")
        else:
            self.media_player.play()
            self.pauseButton.setText("Pause")

    def playback_state_changed(self,state):
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.pauseButton.setText("Play")
            self.nextButton.setEnabled(True)

    def replay_video(self):
        self.media_player.setPosition(0)
        self.media_player.play()
        self.pauseButton.setText("Pause")

    def next_page(self):
        self.media_player.stop()
        self.parent().next_page()


