from .User import current_user
from datetime import datetime
from pathlib import Path
import csv
from random import randint
import os
#DATA_PATH = "\\\\datadepot.rcac.purdue.edu\\depot\\sbrunswi\\data"
DATA_PATH = "C:\\Users\\jimmy\\Desktop\\Windracers---Efficient-and-safe-HAT-main\\TestDataStorage"
class UserController(object):
    def login(self):
        # with open(f"{DATA_PATH}\\credentials.csv", 'r') as file:
        #     reader = csv.reader(file)
        #     credentials = {rows[0]:rows[1] for rows in reader}
        # if not username in credentials or not credentials[username] == password:
        #     return False, "Invalid login credentials"
        
        # with open(f"{DATA_PATH}\\login_log.csv", 'a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([username, datetime.now()])
        
        try:
            current_user.uid = ''.join(str(randint(0, 9)) for _ in range(10))
            while os.path.isdir(current_user.uid):
                current_user.uid = ''.join(str(randint(0, 9)) for _ in range(10))
            current_user.start_time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            current_user.data_path = f"{DATA_PATH}\\{current_user.uid}"
            current_user.clicks_path = f"{current_user.data_path}\\clicks_data"
            Path(current_user.data_path).mkdir(parents=True)
            Path(current_user.clicks_path).mkdir()
            Path(f"{current_user.data_path}\\EEG_data").mkdir()
            Path(f"{current_user.data_path}\\GSR_data").mkdir()
            Path(f"{current_user.data_path}\\Cognitive_tasks").mkdir()
            Path(f"{current_user.data_path}\\eye_tracker_data").mkdir()
            Path(f"{current_user.data_path}\\videos").mkdir()
            Path(f"{current_user.data_path}\\html_tasks").mkdir()
            return True, current_user.uid
        except Exception as e:
            return False, str(e)