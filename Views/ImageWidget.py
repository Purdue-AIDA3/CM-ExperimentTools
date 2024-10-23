from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QColor, QFont, QMouseEvent, QPixmap, QImage, QPen
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtMultimediaWidgets import QVideoWidget

class ImageWidget(QLabel):
    def __init__(self, controller, parent=None):
        super().__init__("", parent=parent)
        self.controller = controller

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.controller.insert_click(event.pos().x(), event.pos().y())
            self.update()
 
    def paintEvent(self, event):
        super().paintEvent(event)
        pixmap = QPixmap("Resources/undo.png")
        painter = QPainter(self)
        painter.drawPixmap(0,0, pixmap)
        points = self.controller.get_points()
        if len(points)>0:
            for i, point in enumerate(points):
                if i%2==0 and len(points)>i+1:
                    pen = QPen(Qt.GlobalColor.blue) 
                    pen.setWidth(3)
                    painter.setPen(pen)
                    next_point = points[i+1]
                    painter.drawLine(point.x, point.y, next_point.x, next_point.y)
                painter.setPen(Qt.GlobalColor.black)
                painter.setFont(QFont('Arial', 12))
                rect = QRectF(point.x-15, point.y-15, 30, 30)
                painter.fillRect(rect, Qt.GlobalColor.blue)
                painter.setPen(Qt.GlobalColor.black)
                painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
                painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter, str(i+1))
            