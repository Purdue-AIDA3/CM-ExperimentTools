import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QSizePolicy, QGridLayout, QSpacerItem, QMessageBox, QDialog, QHBoxLayout, QRadioButton, QButtonGroup, QStackedLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QFont, QGuiApplication
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from Controllers.Task2Controller import Task2Controller
from .Task2WebEngineView import Task2WebEngineView

class ConfirmationDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Confirmation")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel('Are you sure you have finished the task?', self)
        layout.addWidget(self.label)
        control_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm)
        control_layout.addWidget(self.confirm_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        control_layout.addWidget(self.cancel_button)
        layout.addLayout(control_layout)
        
    def confirm(self):
        self.accept()

class ISA(QWidget):
    def __init__(self, controller, task2_window, parent=None):
        super().__init__(parent)
        self.task2_window = task2_window
        self.controller = controller
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.init_ui()
        qtRectangle = self.frameGeometry()
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        qtRectangle.setX(0)
        qtRectangle.setY(-25)
        self.setGeometry(qtRectangle)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)

    def init_ui(self,):
        self.main_layout = QStackedLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.start_button.clicked.connect(self.start)
        self.main_layout.addWidget(self.start_button)
        container_widget = QWidget()
        layout = QGridLayout(container_widget)        
        self.main_layout.addWidget(container_widget)
        self.group = QButtonGroup()
        self.group.setExclusive(False)
        self.group.buttonClicked.connect(self.on_radio_button_toggled)
        self.buttons = [QRadioButton(f"{i+1}", self) for i in range(5)]
        space = 50
        #layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),0,0, 1, space)
        for i,button in enumerate(self.buttons):
            layout.addWidget(button, 0, i)
            button.setFont(QFont("Arial", 20))
            button.setStyleSheet("QRadioButton::indicator { width: 30px; height: 30px; background-color: red;}")
            self.group.addButton(button)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),0,len(self.buttons), 1, space)
        self.setLayout(self.main_layout)
        self.setFixedHeight(50)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_isa)

    def on_radio_button_toggled(self, radio_button):
        sender = self.sender()
        for button in self.buttons:
            if button is not radio_button:
                button.setChecked(False)
        
        isa = radio_button.text()
        self.controller.insert_isa(isa)
        radio_button.setChecked(False)
        self.main_layout.setCurrentIndex(0)

    def get_isa(self):
        self.main_layout.setCurrentIndex(1)
        self.timer.start(60000)
    
    def start(self):
        self.timer.start(60000)
        self.main_layout.insertWidget(0, QWidget())
        self.main_layout.setCurrentIndex(0)
        self.main_layout.removeWidget(self.start_button)
        self.controller.add_start_time()
        if self.task2_window.audio_files != None: #TODO do this with a signal
            self.task2_window.timer.start(15000)

class Task2B(QWidget):
    def __init__(self, parent=None, audio_files=None, two_windows=False, isa = True):
        super().__init__(parent)
        self.setWindowTitle('Task 2')
        self.audio_files = audio_files
        task_name = "Task2"
        if two_windows:
            task_name += "_two_platforms"
        else:
            task_name += "_one_platform"
        if audio_files != None:
            task_name += "_secondary"
        self.controller = Task2Controller(task_name)
        self.current_audio_file = 0
        self.init_ui(two_windows, isa)

    def init_ui(self, two_windows, isa):
        layout = QGridLayout()
        self.title_label = QLabel(f'Please let the staff open the corresponding google chrome window for this task. ', self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.confirm)
        if isa:
            self.isa = ISA(self.controller, self)
            self.isa.show()
        else:
            self.isa = None

        if self.audio_files != None:
            self.timer = QTimer(self)
            self.audio_output = QAudioOutput()
            self.audio_player = QMediaPlayer()
            self.audio_player.setAudioOutput(self.audio_output)
            self.audio_output.setVolume(50)
            self.timer.timeout.connect(self.play_audio)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),0,0)
        layout.addWidget(self.title_label, 1,0)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),2,0)
        layout.addWidget(self.next_button, 3,0)

        self.setLayout(layout)
        self.parent().showMaximized()

    def play_audio(self):
        if self.current_audio_file == len(self.audio_files):
            return
        self.audio_player.setSource(QUrl.fromLocalFile(self.audio_files[self.current_audio_file]))
        self.audio_player.play()
        self.current_audio_file += 1
        self.timer.start(15000)

    def confirm(self):
        confirmation_dialog = ConfirmationDialog()
        if confirmation_dialog.exec() == QDialog.DialogCode.Accepted:
            self.next_page()

    def next_page(self):
        self.controller.save_data()
        if self.isa != None:
            self.isa.close()
        self.isa = None
        if self.audio_files != None:
            self.timer.stop()
        self.parent().next_page()
