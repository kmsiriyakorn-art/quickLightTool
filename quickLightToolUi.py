try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
	from PySide6.QtCore import QSize 
	from PySide6.QtGui import QColor


except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
	from PySide2.QtCore import QSize 
	from PySide2.QtGui import QColor
	
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import importlib
from . import wheel
from . import quickLightToolUtil as qlutil
importlib.reload(wheel)
importlib.reload(qlutil)
import os

class QuickLightDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.resize(300, 350)
		self.setWindowTitle('Quick Ligthing Tool')

		self.mainLayout = QtWidgets.QVBoxLayout() # layout
		self.setLayout(self.mainLayout)

		self.typeLayout = QtWidgets.QVBoxLayout() 
		self.mainLayout.addLayout(self.typeLayout)

		self.colorWheel = wheel.SimpleColorWheel(100)
		self.mainLayout.addWidget(self.colorWheel, alignment=QtCore.Qt.AlignCenter)


		self.colorListLayout = QtWidgets.QGridLayout() 
		self.mainLayout.addLayout(self.colorListLayout)

		self.buttonLayout = QtWidgets.QHBoxLayout() 
		self.sizeLayout = QtWidgets.QGridLayout() 
	
		self.typeLabel = QtWidgets.QLabel('Color Harmony :') # label
		self.typeCombobox = QtWidgets.QComboBox()
		self.typeCombobox.addItems(['Analogous','Complementary','Split Complementary','Triad'])
		self.colorLabel = QtWidgets.QLabel('Color')
		self.lightLabel = QtWidgets.QLabel('Light')
		self.intensityLabel = QtWidgets.QLabel('Intensity')
		self.expLabel = QtWidgets.QLabel('Exposure')

		self.colorBox1 = QtWidgets.QPushButton()        #list's widgets
		self.colorBox1.setFixedSize(QSize(30,30)) 	
		self.lightCombobox1 = QtWidgets.QComboBox()
		self.lightCombobox1.addItems(['key','fill','back'])
		self.lightCombobox1.setCurrentText('key')
		self.intensityLineEdit1 = QtWidgets.QLineEdit()
		self.intensityLineEdit1.setText("10")
		self.expLineEdit1 = QtWidgets.QLineEdit()
		self.expLineEdit1.setText("8")
		self.selectCheckBox1 = QtWidgets.QCheckBox()
		self.selectCheckBox1.setChecked(True)
		
		self.colorBox2 = QtWidgets.QPushButton()
		self.colorBox2.setFixedSize(QSize(30,30))
		self.lightCombobox2 = QtWidgets.QComboBox()
		self.lightCombobox2.addItems(['key','fill','back'])
		self.lightCombobox2.setCurrentText('fill')
		self.intensityLineEdit2 = QtWidgets.QLineEdit()
		self.intensityLineEdit2.setText("10")
		self.expLineEdit2 = QtWidgets.QLineEdit()
		self.expLineEdit2.setText("8")
		self.selectCheckBox2 = QtWidgets.QCheckBox()
		self.selectCheckBox2.setChecked(True)
		
		self.colorBox3 = QtWidgets.QPushButton()
		self.colorBox3.setFixedSize(QSize(30,30))
		self.lightCombobox3 = QtWidgets.QComboBox()
		self.lightCombobox3.addItems(['key','fill','back'])
		self.lightCombobox3.setCurrentText('back')
		self.intensityLineEdit3 = QtWidgets.QLineEdit()
		self.intensityLineEdit3.setText("10")
		self.expLineEdit3 = QtWidgets.QLineEdit()
		self.expLineEdit3.setText("8")
		self.selectCheckBox2.setChecked(True)
		self.selectCheckBox3 = QtWidgets.QCheckBox() 	
		self.selectCheckBox3.setChecked(True) 

		self.lightSizeLabel = QtWidgets.QLabel('Light Size :')
		self.lightSizeSpinBox = QtWidgets.QSpinBox()
		self.lightSizeSpinBox.setFixedSize(QSize(70,20))
		self.lightSizeSpinBox.setMinimum(1)
		self.lightSizeLabel2 = QtWidgets.QLabel('* bigger light = less brightness * \n* increase the intensity and exposure for visible brightness *',alignment=QtCore.Qt.AlignCenter)
		
		usLocale = QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates)
		self.lightSizeSpinBox.setLocale(usLocale)

		self.delAllbutton = QtWidgets.QPushButton("delete created light")
		self.delAllbutton.clicked.connect(self.deleteLight)

		
		self.currentColors = {
			self.colorBox1: QtGui.QColor("white"),
			self.colorBox2: QtGui.QColor("white"),
			self.colorBox3: QtGui.QColor("white")
		}

		

		self.createButton = QtWidgets.QPushButton('create')
		self.cancelButton = QtWidgets.QPushButton('cancel')

		
		self.typeLayout.addWidget(self.typeLabel)         # add widgets
		self.typeLayout.addWidget(self.typeCombobox)


		self.colorListLayout.addWidget(self.colorLabel,0,1,alignment=QtCore.Qt.AlignCenter)
		self.colorListLayout.addWidget(self.lightLabel,0,2,alignment=QtCore.Qt.AlignCenter)
		self.colorListLayout.addWidget(self.intensityLabel,0,3,alignment=QtCore.Qt.AlignCenter)
		self.colorListLayout.addWidget(self.expLabel,0,4,alignment=QtCore.Qt.AlignCenter)
		
		self.colorListLayout.addWidget(self.lightCombobox1,1,2)
		self.colorListLayout.addWidget(self.lightCombobox2,2,2)
		self.colorListLayout.addWidget(self.lightCombobox3,3,2)
		
		self.colorListLayout.addWidget(self.intensityLineEdit1,1,3,alignment=QtCore.Qt.AlignCenter)
		self.colorListLayout.addWidget(self.intensityLineEdit2,2,3,alignment=QtCore.Qt.AlignCenter)
		self.colorListLayout.addWidget(self.intensityLineEdit3,3,3,alignment=QtCore.Qt.AlignCenter)

		self.colorListLayout.addWidget(self.selectCheckBox1,1,5)
		self.colorListLayout.addWidget(self.selectCheckBox2,2,5)
		self.colorListLayout.addWidget(self.selectCheckBox3,3,5)

		self.colorListLayout.addWidget(self.expLineEdit1,1,4)
		self.colorListLayout.addWidget(self.expLineEdit2,2,4)
		self.colorListLayout.addWidget(self.expLineEdit3,3,4)
		
		self.colorListLayout.addWidget(self.colorBox1,1,1,alignment=QtCore.Qt.AlignCenter)
		self.colorListLayout.addWidget(self.colorBox2,2,1,alignment=QtCore.Qt.AlignCenter)
		self.colorListLayout.addWidget(self.colorBox3,3,1,alignment=QtCore.Qt.AlignCenter)
		
		self.sizeLayout.addWidget(self.lightSizeLabel,0,1,alignment=QtCore.Qt.AlignCenter)
		self.sizeLayout.addWidget(self.lightSizeSpinBox,0,2,alignment=QtCore.Qt.AlignCenter)
		self.mainLayout.addLayout(self.sizeLayout,alignment=QtCore.Qt.AlignCenter)
		self.mainLayout.addWidget(self.lightSizeLabel2,alignment=QtCore.Qt.AlignCenter)
		self.mainLayout.addWidget(self.delAllbutton)
		self.buttonLayout.addWidget(self.createButton)
		self.buttonLayout.addWidget(self.cancelButton)
		self.mainLayout.addLayout(self.buttonLayout)
		
		self.colorBox1.clicked.connect(lambda: self.manualPick(self.colorBox1))
		self.colorBox2.clicked.connect(lambda: self.manualPick(self.colorBox2))
		self.colorBox3.clicked.connect(lambda: self.manualPick(self.colorBox3))
		
		self.typeCombobox.currentTextChanged.connect(self.change_harmony_mode)

		self.createButton.clicked.connect(self.create_selected_lights)
		self.cancelButton.clicked.connect(self.close)
		# --- connect wheel signal to update the box ---
		self.colorWheel.colorSelected.connect(self.on_color_changed)
		# keep a reference to the currently selected color
		self.currentColor = QtGui.QColor(255, 255, 255)

	def manualPick(self, color_box):     #เลือกสีเอง แต่ละกล่อง
		start_color = self.currentColors.get(color_box, QtGui.QColor("white"))
		color = QtWidgets.QColorDialog.getColor(start_color, self, "Pick Light Color")
		if color.isValid():
			self.currentColors[color_box] = color
			color_box.setStyleSheet(f"QPushButton{{background-color: {color.name()};}}")
		for box, color in self.currentColors.items():
			print(f"{box.objectName() if hasattr(box, 'objectName') else box}: {color.name()}")
			
	
	def update_color_boxes(self, colors: list[QtGui.QColor]): #อัพเดทอัตโนมัติ 3กล่อง ใช้ loop ,รับ ลิสต์สีมาจาก emit ,กำหนดลิสต์กล่องเอง
		boxes = [self.colorBox1, self.colorBox2, self.colorBox3]  
		for box, color in zip(boxes, colors):
			self.currentColors[box] = color
			box.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")

	def change_harmony_mode(self, mode_text):
		self.colorWheel.harmony_mode = mode_text.lower()
		self.colorWheel.update()

	def on_color_changed(self, color: QtGui.QColor):
		colors = self.colorWheel.get_harmony_colors()
		self.update_color_boxes(colors)
	
	def create_selected_lights(self):
		"""Create lights for all checked boxes using their own role combo and color."""


		# --- BOX 1 ---
		if self.selectCheckBox1.isChecked():
			role = self.lightCombobox1.currentText()
			color = self.currentColors[self.colorBox1]
			name = role + "_light"
			intens = float(self.intensityLineEdit1.text())
			exp = float(self.expLineEdit1.text())
			size = int(self.lightSizeSpinBox.value())
			qlutil.create_light_by_role(name , role, color, intens ,exp, size)
			print(color)

		# --- BOX 2 ---
		if self.selectCheckBox2.isChecked():
			role = self.lightCombobox2.currentText()
			color = self.currentColors[self.colorBox2]
			name = role + "_light"
			intens = float(self.intensityLineEdit2.text())
			exp = float(self.expLineEdit2.text())
			size = int(self.lightSizeSpinBox.value())
			qlutil.create_light_by_role(name, role, color, intens , exp, size)

		# --- BOX 3 ---
		if self.selectCheckBox3.isChecked():
			role = self.lightCombobox3.currentText()
			color = self.currentColors[self.colorBox3]
			name = role + "_light"
			intens = float(self.intensityLineEdit3.text())
			size = int(self.lightSizeSpinBox.value())
			exp = float(self.expLineEdit3.text())
			
			qlutil.create_light_by_role(name, role, color, intens, exp, size)

	def deleteLight(self):
		my_lights = cmds.ls("key_light*", "fill_light*", "back_light*", type="aiAreaLight")	
		if my_lights:
			cmds.delete(my_lights)

		empty_Groups = cmds.ls("key_light*", "fill_light*", "back_light*", type="transform")	
		if empty_Groups:
			cmds.delete(empty_Groups)






	
def run():
	global ui
	try:
		ui.close()
	except:
		pass

	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = QuickLightDialog(parent=ptr)
	ui.show()
	

