try:
	from PySide6 import QtWidgets, QtGui, QtCore
except:
	from PySide2 import QtWidgets, QtGui, QtCore
import math
import importlib


class SimpleColorWheel(QtWidgets.QWidget):
	colorSelected = QtCore.Signal(QtGui.QColor)

	def __init__(self, radius=120, harmony_mode="analogous"):   
		super(SimpleColorWheel, self).__init__()
		self.radius = radius
		self.harmony_mode = harmony_mode 
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
		painter.setBrush(QtCore.Qt.white)
		painter.setPen(QtGui.QPen(QtGui.QColor("black"), 1))


		# always draw the selected hue indicator
		indicator_offset = 20
		angle_rad = math.radians(self.current_angle)
		px = cx + (self.radius-indicator_offset) * math.cos(angle_rad)
		py = cy - (self.radius-indicator_offset) * math.sin(angle_rad)
		painter.drawEllipse(QtCore.QPointF(px, py), 10, 10)

		harmony_angles = []
		if self.harmony_mode == "complementary":
			harmony_angles = [(self.current_angle + 180) % 360]

		elif self.harmony_mode == "analogous":
			harmony_angles = [
				(self.current_angle + 30) % 360,
				(self.current_angle - 30) % 360,
			]
		elif self.harmony_mode == "triad":
			harmony_angles = [
				(self.current_angle + 120) % 360,
				(self.current_angle + 240) % 360,
			]

		elif self.harmony_mode == "split complementary":
			harmony_angles = [
				(self.current_angle + 210) % 360,
				(self.current_angle + 150) % 360,
			]

		
		for h_angle in harmony_angles:
			rad = math.radians(h_angle)
			px_h = cx + (self.radius-indicator_offset) * math.cos(rad)
			py_h = cy - (self.radius-indicator_offset) * math.sin(rad)
			painter.drawEllipse(QtCore.QPointF(px_h, py_h), 10, 10)


	def _update_color(self, pos):
		dx = pos.x() - self.width() / 2
		dy = pos.y() - self.height() / 2
		angle = (math.degrees(math.atan2(-dy, dx)) + 360) % 360
		self.current_angle = angle
		
		self.selected_color = QtGui.QColor.fromHsv(int(angle), 255, 255)
		self.colorSelected.emit(self.selected_color)
		self.update()

	def get_harmony_angles(self):
		a = self.current_angle
		if self.harmony_mode == "complementary":
			return [a, (a + 180) % 360]
		elif self.harmony_mode == "triad":
			return [a, (a + 120) % 360, (a + 240) % 360]
		elif self.harmony_mode == "analogous":
			return [a, (a - 30) % 360, (a + 30) % 360]
		elif self.harmony_mode == "split complementary":
			return [a, (a + 210) % 360, (a + 150) % 360]
		else:
			return [a]
	
	def get_harmony_colors(self):
		return [QtGui.QColor.fromHsv(int(angle), 255, 255)
			for angle in self.get_harmony_angles()]        

	def mousePressEvent(self, event):
		self.dragging = True
		self._update_color(event.pos())

	def mouseMoveEvent(self, event):
		if self.dragging:
			self._update_color(event.pos())

	def mouseReleaseEvent(self, event):
		from . import quickLightToolUi
		from .quickLightToolUi import QuickLightDialog
		importlib.reload(quickLightToolUi)
		ui = QuickLightDialog()
		self.dragging = False
		colors = self.get_harmony_colors()

		ui.update_color_boxes(colors)
		for box, color in ui.currentColors.items():
			print(box.objectName(), color.name())
		print("\n")



