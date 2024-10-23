from Models import *
from .User import current_user
from datetime import datetime
import json

class Task1Controller(object):
    def __init__(self, task_name):
        self.model = Task1ClicksModel(task_name)

    def add_start_time(self):
        self.model.start_time = str(datetime.now())

    def add_end_time(self):
        self.model.end_time = str(datetime.now())

    def insert_click(self, new_x, new_y):
        time = str(datetime.now())
        action = Action.ADD_POINT
        if new_x >= 0 and new_x <= 50 and new_y >= 0 and new_y <= 50:
            action = Action.UNDO

        if action == Action.ADD_POINT:
            self.model.saved_points.append(Point(new_x, new_y))
        elif action == Action.UNDO and len(self.model.saved_points)>0:
            self.model.saved_points.pop()
        self.model.clicks.append(Click(new_x, new_y, time, action))

    def get_points(self):
        return self.model.saved_points

    def save_data(self):
        task1_data = {
            "video_start_time": self.model.start_time,
            "video_end_time": self.model.end_time,
            "clicks": [click.to_dict() for click in self.model.clicks],
            "saved_points": [point.to_dict() for point in self.model.saved_points]
        }
        with open(f"{current_user.clicks_path}\\{self.model.task_name}.json", 'w') as f:
            json.dump(task1_data, f, indent=4)