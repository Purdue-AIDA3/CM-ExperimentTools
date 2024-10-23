from PyQt6.QtWidgets import QStackedWidget, QMainWindow
from PyQt6.QtCore import Qt
from .Login import Login
from .SurveyWindow import SurveyWindow
from .VideoPlayer import VideoPlayer
from .Welcome import Welcome
from .Task1 import Task1
from .Task1Clicks import Task1Clicks
#from .Task2 import Task2
from .Task2B import Task2B
from .Instructions import Instructions
import glob
import random
import csv
from .Break import Break
from .Thanks import Thanks

class MainWindow(QStackedWidget, QMainWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.windows_list = [("Login screen", Login),
                             ("Intake Survey", self.get_survey("SV_0qdc3A6fsdViGR8")), 
                             ("Welcome Screen", Welcome), 
                             ("Task 1 Instructions" , self.get_video_player("Task 1 Instructions", "./Resources/Task_1_Training.mp4")),]
        self.controller = controller
        task1_names = glob.glob("Resources/Task_1/*.mp4")
        random.shuffle(task1_names)
        for i in range(15):
            name = task1_names[i]
            task_id = name.replace(".mp4", "").replace("Resources/Task_1\\", "")
            self.windows_list += [(f"Task 1 Video for {task_id}", self.get_task1(task_id)), (f"NASA TLX for {task_id}", self.get_survey("SV_0kP9iQpsp33Y4lg", metadata={"taskid": task_id}))]
        
        self.windows_list.append(("Secondary Task Instruction", self.get_video_player("Secondary Task Instructions", "./Resources/Secondary_Task_Training.mp4")))
        
        task_1_audio_files = []
        with open("Resources/Secondary_Task/Task_1/Task_1_Words.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                task_1_audio_files.append(f"Resources/Secondary_Task/Task_1/{row[0]}.mp4")
        j = 0
        for i in range(15,30):
            name = task1_names[i]
            task_id = name.replace(".mp4", "").replace("Resources/Task_1\\", "")
            self.windows_list += [(f"Task 1 Video for {task_id} with secondary task", self.get_task1_secondary(task_id, [task_1_audio_files[j], task_1_audio_files[j+1]])), (f"NASA TLX for {task_id} with secondary task", self.get_survey("SV_0kP9iQpsp33Y4lg", metadata={"taskid": f"{task_id}_secondary"}))]
            j += 2
        task_2_1_audio_files = []
        task_2_2_audio_files = []
        with open("Resources/Secondary_Task/Task_2/Task_2_Words.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                task_2_1_audio_files.append(f"Resources/Secondary_Task/Task_2/{row[0]}.mp4")
                task_2_2_audio_files.append(f"Resources/Secondary_Task/Task_2/{row[1]}.mp4")

        self.windows_list.append(("Break", Break))
        task2_training_files = []
        with open("Resources/Task_2_Training/order.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                task2_training_files.append(f"Resources/Task_2_Training/{row[0]}.mp4")
        for name in task2_training_files:
            training_name = name.replace(".mp4", "").replace("Resources/Task_2_Training/", "")
            self.windows_list.append((f"Task 2 Training ({training_name})" , self.get_video_player(f"Task 2 Training ({training_name})", name)))


        self.windows_list.append(("Instructions_Task_2_Test", self.get_instructions("After the training video, now you should be able to use the cloud control system! Let’s do a test session where you need to set a mission to make the UAV go around the airport. An example is shown below. First set the user settings. Follow the guidelines when setting the waypoints. Then, move one waypoint and re-upload the mission. Then, arm the UAV and set the mode to auto so the UAV takes off. Finally, try setting a guided point and once the UAV reaches the guided point reset the mode to auto to continue the mission.", "Resources/Task_2_test.png")))
        
        self.windows_list.append(("Instructions_Task_2_Test", self.get_instructions("Select the UAV to control by clicking the tab on the left right corner (shown below). A list of live platforms will appear. Each platform represents a UAV. Select the corresponding ones for your trial. For this trial choose test_trial", "Resources/Task_2_select_UAV.png")))
        self.windows_list.append(("Task_2_Test", self.get_task2_no_isa()))

        self.windows_list.append(("Instructions_Task_2", self.get_instructions("For task 2 there are four scenarios, task 2 with one UAV, task 2 with one UAV with secondary task, task 2 with two UAVs, and task 2 with two UAVs with secondary task. Also, you need to do instantaneous self-assessment (ISA) every minute. For ISA, five buttons will appear at the top that show numbers from 1 to 5. You need to click the number that most accurately represents your perceived workload. 1 means the lowest workload and 5 means the highest workload. After clicking, the window will disappear and it will appear again after one minute. Whenever there is an intruder, set a guided point to resolve the conflict. Once the conflict is resolved, set the flight mode to auto mode.")))
        self.windows_list.append(("Instructions_Task_2_one_platform", self.get_instructions("For the first task, you are required to fly UAV 'trial1_Purdue_Dahnke' from Purdue Airport to Dahnke Airport without the secondary task. \nThere will be a UAV parked at each airport, so you can look for the White UAVs to locate all airports. On the next window, when you are ready to begin click start.")))
        self.windows_list.append(("Task_2_one_platform", Task2B))
        self.windows_list.append((f"NASA TLX for Task2 with one platform", self.get_survey("SV_0kP9iQpsp33Y4lg", metadata={"taskid": "Task_2_one_platform"})))
        self.windows_list.append(("Break", Break))

        self.windows_list.append(("Instructions_Task_2_one_platform_secondary", self.get_instructions("For the second task, you are required to fly UAV 'trial1_sec_Purdue_Dahnke' from Purdue Airport to Dahnke Airport with the secondary task. \nThere will be a UAV parked at each airport, so you can look for the White UAVs to locate all airports. On the next window, when you are ready to begin click start.")))
        self.windows_list.append(("Task_2_one_platform_secondary", self.get_task2_secondary(task_2_1_audio_files)))
        self.windows_list.append((f"NASA TLX for Task2 with one platform with secondary task", self.get_survey("SV_0kP9iQpsp33Y4lg", metadata={"taskid": "Task_2_one_platform_secondary"})))
        self.windows_list.append(("Break", Break))

        self.windows_list.append(("Instructions_Task_2_two_platforms", self.get_instructions("For the third task, you are required to fly UAV 'trial2_Purdue_Wyandotte' from Purdue Airport to Wyandotte Airport and UAV 'trial2_Purdue_TimberHouse' from Purdue Airport to Timber House Airport without the secondary task. \nThere will be a UAV parked at each airport, so you can look for the White UAVs to locate all airports. On the next window, when you are ready to begin click start.")))
        self.windows_list.append(("Task_2_two_platforms", self.get_task2_2()))
        self.windows_list.append((f"NASA TLX for Task2 with two platforms", self.get_survey("SV_0kP9iQpsp33Y4lg", metadata={"taskid": "Task_2_two_platforms"})))
        self.windows_list.append(("Break", Break))

        self.windows_list.append(("Instructions_Task_2_two_platforms_secondary", self.get_instructions("For the fourth task, you are required to fly UAV 'trial2_sec_Purdue_Wyandotte' from Purdue Airport to Wyandotte Airport and UAV 'trial2_sec_Purdue_TimberHouse' from Purdue Airport to Timber House Airport with the secondary task. \nThere will be a UAV parked at each airport, so you can look for the White UAVs to locate all airports. On the next window, when you are ready to begin click start")))
        self.windows_list.append(("Task_2_two_platforms_secondary", self.get_task2_2_secondary(task_2_2_audio_files)))
        self.windows_list.append((f"NASA TLX for Task2 with two platforms with secondary task", self.get_survey("SV_0kP9iQpsp33Y4lg", metadata={"taskid": "Task_2_two_platforms_secondary"})))
        self.windows_list.append(("Thanks", Thanks))
        self.current_page = 0
        self.controller.window_start(self.windows_list[self.current_page][0])
        self.addWidget(self.windows_list[self.current_page][1](self))
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        #self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
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
            return Instructions(instructions,parent, image)
        return __thunk

    def get_task1_secondary(self, file, audio_files):
        def __thunk(parent):
            return Task1(file, parent, audio_files)
        return __thunk

    def get_task2_secondary(self, audio_files):
        def __thunk(parent):
            return Task2B(parent, audio_files)
        return __thunk

    def get_task2_no_isa(self):
        def __thunk(parent):
            return Task2B(parent, isa=False)
        return __thunk

    def get_task2_2(self):
        def __thunk(parent):
            return Task2B(parent, two_windows=True)
        return __thunk

    def get_task2_2_secondary(self, audio_files):
        def __thunk(parent):
            return Task2B(parent, audio_files, two_windows=True)
        return __thunk

    def get_survey(self, survey, metadata=None):
        def __thunk(parent):
            return SurveyWindow(survey, parent, metadata=metadata)
        return __thunk

    def next_page(self):
        self.controller.window_end(self.windows_list[self.current_page][0])
        self.current_page += 1
        if self.current_page == len(self.windows_list):
            self.close()
            return
        self.controller.window_start(self.windows_list[self.current_page][0])
        self.addWidget(self.windows_list[self.current_page][1](self))
        self.removeWidget(self.currentWidget())

    def insert_widget(self, widget):
        self.windows_list.insert(self.current_page+1, widget)
        self.next_page()


