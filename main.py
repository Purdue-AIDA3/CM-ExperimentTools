from Views.MainWindow import MainWindow
from Controllers.WindowsController import WindowsController
from Controllers.TriggerController import TriggerController
import sys
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Set Fusion style
    windows_controller = WindowsController()
    trigger_controller = TriggerController()
    def quit():
        windows_controller.save_data()
        trigger_controller.save_data()
    app.aboutToQuit.connect(quit)
    main_window = MainWindow(windows_controller)
    main_window.show()
    sys.exit(app.exec())