from .User import current_user
from datetime import datetime
import json

class WindowsController(object):
    def __init__(self):
        self.window_list = {}
    
    def window_start(self, window):
        self.window_list[window] = {"start_time": str(datetime.now())}

    def window_end(self, window):
        self.window_list[window]["end_time"] = str(datetime.now())

    def save_data(self):
        with open(f"{current_user.data_path}\\window_times.json", 'w') as f:
            json.dump(self.window_list, f, indent=4)