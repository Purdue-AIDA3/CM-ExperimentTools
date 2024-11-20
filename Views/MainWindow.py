from PyQt6.QtWidgets import QStackedWidget, QMainWindow
from PyQt6.QtCore import Qt
from .Login import Login
from .SurveyWindow import SurveyWindow
from .VideoPlayer import VideoPlayer
from .Welcome import Welcome
from .Task1 import Task1
from .Task1Clicks import Task1Clicks
from .Task1ClicksTimer import Task1ClicksTimer
from .Instructions import Instructions
from pathlib import Path
import os
import glob
import random
import csv
from .TimerNotification import TimerNotification
from .Break import Break
from .Thanks import Thanks
from Controllers.User import current_user
from .PlotDisplay import PlotDisplay

class MainWindow(QStackedWidget, QMainWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        # Initialize windows list with initial screens
        self.windows_list = [
            ("Login screen", Login),
            ("Intake Survey", self.get_survey("SV_cZqUPwWNFmWZczk")),
            ("Welcome Screen", Welcome),
            ("Task 1 Instructions", self.get_video_player("Task 1 Instructions", "./Resources/Task_1_Training.mp4"))
        ]

        # Load and shuffle Task 1 videos
        task1_names = glob.glob("Resources/Task_1/*.mp4")
        random.shuffle(task1_names)

        # Add tasks and PlotDisplay for each video in Set 1
        for i in range(10):
            name = task1_names[i]
            task_id = os.path.basename(name).replace(".mp4", "")
            video_path = f"Resources/Task_1/{task_id}.mp4"
            gt_file = f"./ground_truth/{task_id}.json"
            clicks_file = f"{current_user.clicks_path}/{task_id}.json" if current_user.clicks_path else None

            # Check for missing files
            if not (os.path.exists(video_path) and os.path.exists(gt_file)):
                print(f"Warning: Missing files for task {task_id}. Skipping.")
                continue

            # Debugging logs
            print(f"DEBUG: Adding task {task_id}")
            print(f"DEBUG: Video path: {video_path}")
            print(f"DEBUG: Ground truth path: {gt_file}")
            print(f"DEBUG: Clicks data path: {clicks_file}")

            self.windows_list += [
                (f"Task 1 Video for {task_id}", self.get_task1(task_id)),
                (f"NASA TLX for {task_id}", self.get_survey("SV_bIxjGoogEz3eEqG", metadata={"taskid": task_id}))
            ]

        # Secondary tasks for Set 2
        #self.windows_list.append(("Secondary Task Instruction", self.get_video_player("Secondary Task Instructions", "./Resources/Secondary_Task_Training.mp4")))

        # Load secondary task audio files
        task_1_audio_files = []
        with open("Resources/Secondary_Task/Task_1/Task_1_Words.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                task_1_audio_files.append(f"Resources/Secondary_Task/Task_1/{row[0]}.mp4")

        # Add Set 2 tasks
        j = 0
        for i in range(10, 20):
            name = task1_names[i]
            task_id = os.path.basename(name).replace(".mp4", "")
            if j + 1 >= len(task_1_audio_files):
                print(f"Warning: Not enough audio files for task {task_id}. Skipping.")
                continue

            self.windows_list += [
                (f"Task 1 Video for {task_id} with secondary task", self.get_task1_secondary(task_id, [task_1_audio_files[j], task_1_audio_files[j + 1]])),
                (f"Plot Display for {task_id}", self.get_plot_display(task_id)),
                (f"NASA TLX for {task_id} with secondary task", self.get_survey("SV_bIxjGoogEz3eEqG", metadata={"taskid": f"{task_id}"}))
            ]
            j += 2

        self.windows_list.append(("TimerNotification", TimerNotification))

        # Add Set 3 tasks
        task_1_audio_files_2 = []
        with open("Resources/Secondary_Task/Task_2/Task_2_Words.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                task_1_audio_files_2.append(f"Resources/Secondary_Task/Task_2/{row[0]}.mp4")

        k = 0
        for i in range(20, 30):
            name = task1_names[i]
            task_id = os.path.basename(name).replace(".mp4", "")

            self.windows_list += [
                (f"Task 1 Video for {task_id} with secondary task", self.get_task1_secondary_with_timer(task_id, [task_1_audio_files_2[k], task_1_audio_files_2[k + 1]])),
                (f"Plot Display for {task_id}", self.get_plot_display(task_id)),
                (f"NASA TLX for {task_id} with secondary task", self.get_survey("SV_bIxjGoogEz3eEqG", metadata={"taskid": f"{task_id}"}))
            ]
            k += 2

        # Add the final "Thanks" screen
        self.windows_list.append(("Thanks", Thanks))

        # Initial display setup
        self.current_page = 0
        self.controller.window_start(self.windows_list[self.current_page][0])
        self.addWidget(self.windows_list[self.current_page][1](self))
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)
        self.showMaximized()

    def get_video_player(self, title, file):
        def __thunk(parent):
            return VideoPlayer(title, file, parent)
        return __thunk

    def get_task1(self, file):
        def __thunk(parent):
            return Task1(file, parent)
        return __thunk

    def get_instructions(self, instructions, image=None):
        def __thunk(parent):
            return Instructions(instructions, parent, image)
        return __thunk

    def get_task1_secondary(self, file, audio_files):
        def __thunk(parent):
            return Task1(file, parent, audio_files)
        return __thunk

    def get_task1_secondary_with_timer(self, file, audio_files):
        def __thunk(parent):
            return Task1(file, parent, audio_files, clicks_class=Task1ClicksTimer)
        return __thunk

    def get_plot_display(self, task_id):
        def __thunk(parent):
            return PlotDisplay(task_id, self.next_page, parent)
        return __thunk

    def get_survey(self, survey, metadata=None):
        def __thunk(parent):
            return SurveyWindow(survey, parent, metadata=metadata)
        return __thunk

    def next_page(self):
        try:
            # End tracking for the current page
            self.controller.window_end(self.windows_list[self.current_page][0])

            # Move to the next page
            self.current_page += 1
            if self.current_page == len(self.windows_list):
                print("DEBUG: End of tasks reached. Closing application.")
                self.close()
                return

            # Start tracking for the new page
            self.controller.window_start(self.windows_list[self.current_page][0])
            next_widget = self.windows_list[self.current_page][1](self)

            # Debugging
            print(f"DEBUG: Navigating to page {self.current_page}: {self.windows_list[self.current_page][0]}")

            # Check for missing plot display JSON file (if applicable)
            if "Plot Display" in self.windows_list[self.current_page][0]:
                json_file_path = Path(current_user.data_path) / "position_angle_error_details" / f"{self.windows_list[self.current_page][0].split()[-1]}_errors.json"
                if not json_file_path.exists():
                    print(f"Error: Missing JSON file for plot display: {json_file_path}")
                    self.next_page()  # Skip this page
                    return

            # Update the stacked widget
            self.addWidget(next_widget)
            self.removeWidget(self.currentWidget())
        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            print(f"DEBUG: Current page: {self.current_page}")
            print(f"DEBUG: Windows list: {self.windows_list}")
            self.close()


    def insert_widget(self, widget):
        self.windows_list.insert(self.current_page + 1, widget)
        self.next_page()
