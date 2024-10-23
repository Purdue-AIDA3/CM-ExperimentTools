from Models import *
from .User import current_user
from datetime import datetime
import json

class Task2Controller(object):
    def __init__(self, task_name):
        self.model = Task2Model(task_name)

    def insert_click(self, x, y, text):
        time = str(datetime.now())
        self.model.clicks.append(WebClick(x, y, time, text))

    def add_start_time(self):
        self.model.start_time = str(datetime.now())
        
    def insert_isa(self, level):
        time = str(datetime.now())
        self.model.isa_reports.append(ISAReport(level, time))

    def save_data(self):
        task2_data = {
            "mission_start_time": self.model.start_time,
            "clicks": [click.to_dict() for click in self.model.clicks],
            "isa_reports": [point.to_dict() for point in self.model.isa_reports]
        }
        with open(f"{current_user.clicks_path}\\{self.model.task_name}.json", 'w') as f:
            json.dump(task2_data, f, indent=4)