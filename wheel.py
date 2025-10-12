from PySide2 import QtWidgets, QtGui, QtCore
import math

class SimpleColorWheel(QtWidgets.QWidget):
    colorSelected = QtCore.Signal(QtGui.QColor)

    def __init__(self, radius=120):   #, harmony_mode="complementary"
        super(SimpleColorWheel, self).__init__()
        self.radius = radius
        self.harmony_mode = 0 # can be "complementary", "triad", etc.
        self.setFixedSize(radius * 2, radius * 2)
        self.selected_color = QtGui.QColor(255, 0, 0)
        self.current_angle = 0
        self.dragging = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        cx, cy = self.width() // 2, self.height() // 2

        # Draw hue circle
        for x in range(self.width()):
            for y in range(self.height()):
                dx = x - cx
                dy = y - cy
                r = math.sqrt(dx * dx + dy * dy)
                if r <= self.radius:
                    angle = (math.degrees(math.atan2(-dy, dx)) + 360) % 360
                    color = QtGui.QColor.fromHsv(int(angle), 255, 255)
                    painter.setPen(color)
                    painter.drawPoint(x, y)

        # Draw indicators (for selected + harmony colors)
        painter.setBrush(QtCore.Qt.black)

        # always draw the selected hue indicator
        angle_rad = math.radians(self.current_angle)
        px = cx + self.radius * math.cos(angle_rad)
        py = cy - self.radius * math.sin(angle_rad)
        painter.drawEllipse(QtCore.QPointF(px, py), 6, 6)

        # --- Harmony Mode: Complementary ---
        if self.harmony_mode == "complementary":
            comp_angle = (self.current_angle + 180) % 360
            comp_rad = math.radians(comp_angle)
            px2 = cx + self.radius * math.cos(comp_rad)
            py2 = cy - self.radius * math.sin(comp_rad)
            painter.drawEllipse(QtCore.QPointF(px2, py2), 6, 6)

    def _update_color(self, pos):
        dx = pos.x() - self.width() / 2
        dy = pos.y() - self.height() / 2
        angle = (math.degrees(math.atan2(-dy, dx)) + 360) % 360
        self.current_angle = angle
        
        self.selected_color = QtGui.QColor.fromHsv(int(angle), 255, 255)
        self.colorSelected.emit(self.selected_color)
        self.update()
    

    def mousePressEvent(self, event):
        self.dragging = True
        self._update_color(event.pos())

    def mouseMoveEvent(self, event):
        if self.dragging:
            self._update_color(event.pos())

    def mouseReleaseEvent(self, event):
        self.dragging = False
