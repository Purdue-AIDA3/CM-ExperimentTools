from enum import Enum
import json
class Action (Enum):
    ADD_POINT = 1
    UNDO = 2

class Click(object):
    def __init__(self, x, y, time, action):
        self.x = x
        self.y = y
        self.time = time
        self.action = action

    def to_dict(self):
        return {"x": self.x, "y": self.y, "time": self.time, "action": str(self.action)}

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to_dict(self):
        return {"x": self.x, "y": self.y}


class Task1ClicksModel(object):
    def __init__(self, task_name):
        self.task_name = task_name
        self.start_time = 0
        self.end_time = 0
        self.clicks = []
        self.saved_points = []