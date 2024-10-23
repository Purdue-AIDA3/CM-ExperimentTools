class WebClick(object):
    def __init__(self, x, y, time, text):
        self.x = x
        self.y = y
        self.time = time
        self.text = text

    def to_dict(self):
        return {"x": self.x, "y": self.y, "time": self.time, "text": self.text}

class ISAReport(object):
    def __init__(self, level, time):
        self.level = level
        self.time = time
    def to_dict(self):
        return {"level": self.level, "time": self.time}


class Task2Model(object):
    def __init__(self, task_name):
        self.task_name = task_name
        self.start_time = 0
        self.clicks = []
        self.isa_reports = []