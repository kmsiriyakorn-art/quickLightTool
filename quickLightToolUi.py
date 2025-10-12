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
import importlib
from . import config
from . import wheel
importlib.reload(config)
importlib.reload(wheel)
import os
import math

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
		self.mainLayout.addLayout(self.buttonLayout)


		
		self.typeLabel = QtWidgets.QLabel('Color Harmony :') # label
		self.typeCombobox = QtWidgets.QComboBox()
		self.typeCombobox.addItems(config.TYPE)
		self.colorLabel = QtWidgets.QLabel('Color')
		self.lightLabel = QtWidgets.QLabel('Light')
		self.intensityLabel = QtWidgets.QLabel('Intensity')
		
		self.colorBox1 = QtWidgets.QPushButton()        #list's widgets
		self.colorBox1.setFixedSize(QSize(25,25)) 
		self.lightCombobox1 = QtWidgets.QComboBox()
		self.lightCombobox1.addItems(config.LIGHT)
		self.lightCombobox1.setCurrentIndex(config.LIGHT.index('key light'))
		self.intensityLineEdit1 = QtWidgets.QLineEdit()
		self.selectCheckBox1 = QtWidgets.QCheckBox()
		self.selectCheckBox1.setChecked(True)
		self.colorBox2 = QtWidgets.QPushButton()
		self.colorBox2.setFixedSize(QSize(25,25))
		self.lightCombobox2 = QtWidgets.QComboBox()
		self.lightCombobox2.addItems(config.LIGHT)
		self.lightCombobox2.setCurrentIndex(config.LIGHT.index('fill light'))
		self.intensityLineEdit2 = QtWidgets.QLineEdit()
		self.selectCheckBox2 = QtWidgets.QCheckBox()
		self.selectCheckBox2.setChecked(True)
		self.colorBox3 = QtWidgets.QPushButton()
		self.colorBox3.setFixedSize(QSize(25,25))
		self.lightCombobox3 = QtWidgets.QComboBox()
		self.lightCombobox3.addItems(config.LIGHT)
		self.lightCombobox3.setCurrentIndex(config.LIGHT.index('back light'))
		self.intensityLineEdit3 = QtWidgets.QLineEdit()
		self.selectCheckBox3 = QtWidgets.QCheckBox() 
		self.selectCheckBox3.setChecked(True) 
		

		self.createButton = QtWidgets.QPushButton('create')
		self.cancelButton = QtWidgets.QPushButton('cancel')

		
		self.typeLayout.addWidget(self.typeLabel)         # add widgets
		self.typeLayout.addWidget(self.typeCombobox)


		self.colorListLayout.addWidget(self.colorLabel,0,0)
		self.colorListLayout.addWidget(self.lightLabel,0,1)
		self.colorListLayout.addWidget(self.intensityLabel,0,2)
		
		self.colorListLayout.addWidget(self.lightCombobox1,1,1)
		self.colorListLayout.addWidget(self.intensityLineEdit1,1,2)
		self.colorListLayout.addWidget(self.selectCheckBox1,1,3)
		
		self.colorListLayout.addWidget(self.lightCombobox2,2,1)
		self.colorListLayout.addWidget(self.intensityLineEdit2,2,2)
		self.colorListLayout.addWidget(self.selectCheckBox2,2,3)
		
		self.colorListLayout.addWidget(self.lightCombobox3,3,1)
		self.colorListLayout.addWidget(self.intensityLineEdit3,3,2)
		self.colorListLayout.addWidget(self.selectCheckBox3,3,3)
		
		self.colorListLayout.addWidget(self.colorBox1,1,0)
		self.colorListLayout.addWidget(self.colorBox2,2,0)
		self.colorListLayout.addWidget(self.colorBox3,3,0)

		self.colorBox1.clicked.connect(lambda: self.color_dialog(self.colorBox1))
		self.colorBox2.clicked.connect(lambda: self.color_dialog(self.colorBox2))
		self.colorBox3.clicked.connect(lambda: self.color_dialog(self.colorBox3))


		self.buttonLayout.addWidget(self.createButton)
		self.buttonLayout.addWidget(self.cancelButton)

	def color_dialog(self, color_box):
		color = QtWidgets.QColorDialog.getColor()
		if color.isValid():
			self.chosenColor = color
			color_box.setStyleSheet(f"QPushButton{{background-color: {color.name()};}}")


	
def run():
	global ui
	try:
		ui.close()
	except:
		pass

	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = QuickLightDialog(parent=ptr)
	ui.show()
	