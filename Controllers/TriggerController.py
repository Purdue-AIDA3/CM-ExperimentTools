import time
from datetime import datetime
import serial
import threading
from pynput import mouse
from .User import current_user
import json
        

class TriggerController(object):
    
    def __init__(self):
        self.clicks= []
        try:
            self.port = serial.Serial("COM3")
        except Exception as e:
            print("WARNING: trigger port not found. No triggers will be sent to EEG.")
            self.port = None

        self.listener = mouse.Listener(
            on_click=self.on_click)
        self.listener.start()

    
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.clicks.append({"x" : x, "y" : y, "time": str(datetime.now())})
            if self.port != None:
                self.port.write([0x01])
                time.sleep(0.01)
                self.port.write([0x00])

    def save_data(self):
        with open(f"{current_user.clicks_path}\\clicks.json", 'w') as f:
            json.dump(self.clicks, f, indent=4)


