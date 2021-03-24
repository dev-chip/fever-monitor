# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\cooki\OneDrive\Desktop\fever_monitor\qtgui\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(807, 651)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(150, 400))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.pushButton_start = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_start.sizePolicy().hasHeightForWidth())
        self.pushButton_start.setSizePolicy(sizePolicy)
        self.pushButton_start.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout_2.addWidget(self.pushButton_start)
        self.pushButton_stop = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_stop.setSizePolicy(sizePolicy)
        self.pushButton_stop.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_stop.setFont(font)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.verticalLayout_2.addWidget(self.pushButton_stop)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.frame_fps = QtWidgets.QFrame(self.frame)
        self.frame_fps.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_fps.setObjectName("frame_fps")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_fps)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_fps)
        self.label.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_fps = QtWidgets.QLabel(self.frame_fps)
        self.label_fps.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label_fps.setFont(font)
        self.label_fps.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_fps.setObjectName("label_fps")
        self.horizontalLayout_3.addWidget(self.label_fps)
        self.verticalLayout_2.addWidget(self.frame_fps)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.pushButton_settings = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_settings.sizePolicy().hasHeightForWidth())
        self.pushButton_settings.setSizePolicy(sizePolicy)
        self.pushButton_settings.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_settings.setFont(font)
        self.pushButton_settings.setObjectName("pushButton_settings")
        self.verticalLayout_2.addWidget(self.pushButton_settings)
        self.horizontalLayout.addWidget(self.frame)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label_thermal_stream = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_thermal_stream.sizePolicy().hasHeightForWidth())
        self.label_thermal_stream.setSizePolicy(sizePolicy)
        self.label_thermal_stream.setMinimumSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_thermal_stream.setFont(font)
        self.label_thermal_stream.setAlignment(QtCore.Qt.AlignCenter)
        self.label_thermal_stream.setObjectName("label_thermal_stream")
        self.horizontalLayout.addWidget(self.label_thermal_stream)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(300, 125))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_4.setMaximumSize(QtCore.QSize(100, 100))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2.addWidget(self.frame_4)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_6.setMaximumSize(QtCore.QSize(100, 100))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_2)
        self.frame_7.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_7.setMaximumSize(QtCore.QSize(100, 100))
        self.frame_7.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2.addWidget(self.frame_7)
        self.frame_9 = QtWidgets.QFrame(self.frame_2)
        self.frame_9.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_9.setMaximumSize(QtCore.QSize(100, 100))
        self.frame_9.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_2.addWidget(self.frame_9)
        self.frame_8 = QtWidgets.QFrame(self.frame_2)
        self.frame_8.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_8.setMaximumSize(QtCore.QSize(100, 100))
        self.frame_8.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_2.addWidget(self.frame_8)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_5.setMaximumSize(QtCore.QSize(100, 100))
        self.frame_5.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_3.setMaximumSize(QtCore.QSize(100, 100))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame_2)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 807, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuDeveloper = QtWidgets.QMenu(self.menuBar)
        self.menuDeveloper.setObjectName("menuDeveloper")
        self.menuLog_Level_2 = QtWidgets.QMenu(self.menuDeveloper)
        self.menuLog_Level_2.setObjectName("menuLog_Level_2")
        MainWindow.setMenuBar(self.menuBar)
        self.actionDISABLE2 = QtWidgets.QAction(MainWindow)
        self.actionDISABLE2.setCheckable(True)
        self.actionDISABLE2.setObjectName("actionDISABLE2")
        self.actionWARNING2 = QtWidgets.QAction(MainWindow)
        self.actionWARNING2.setCheckable(True)
        self.actionWARNING2.setObjectName("actionWARNING2")
        self.actionINFO2 = QtWidgets.QAction(MainWindow)
        self.actionINFO2.setCheckable(True)
        self.actionINFO2.setObjectName("actionINFO2")
        self.actionDEBUG2 = QtWidgets.QAction(MainWindow)
        self.actionDEBUG2.setCheckable(True)
        self.actionDEBUG2.setObjectName("actionDEBUG2")
        self.actionVERBOSE2 = QtWidgets.QAction(MainWindow)
        self.actionVERBOSE2.setCheckable(True)
        self.actionVERBOSE2.setObjectName("actionVERBOSE2")
        self.action_show_log_view = QtWidgets.QAction(MainWindow)
        self.action_show_log_view.setCheckable(True)
        self.action_show_log_view.setObjectName("action_show_log_view")
        self.actionDISABLE = QtWidgets.QAction(MainWindow)
        self.actionDISABLE.setCheckable(True)
        self.actionDISABLE.setObjectName("actionDISABLE")
        self.actionWARNING = QtWidgets.QAction(MainWindow)
        self.actionWARNING.setCheckable(True)
        self.actionWARNING.setObjectName("actionWARNING")
        self.actionINFO = QtWidgets.QAction(MainWindow)
        self.actionINFO.setCheckable(True)
        self.actionINFO.setObjectName("actionINFO")
        self.actionDEBUG = QtWidgets.QAction(MainWindow)
        self.actionDEBUG.setCheckable(True)
        self.actionDEBUG.setObjectName("actionDEBUG")
        self.actionVERBOSE = QtWidgets.QAction(MainWindow)
        self.actionVERBOSE.setCheckable(True)
        self.actionVERBOSE.setObjectName("actionVERBOSE")
        self.actionShow_model_confidence_instead_of_face_temperature = QtWidgets.QAction(MainWindow)
        self.actionShow_model_confidence_instead_of_face_temperature.setCheckable(True)
        self.actionShow_model_confidence_instead_of_face_temperature.setObjectName("actionShow_model_confidence_instead_of_face_temperature")
        self.menuLog_Level_2.addAction(self.actionDISABLE)
        self.menuLog_Level_2.addAction(self.actionWARNING)
        self.menuLog_Level_2.addAction(self.actionINFO)
        self.menuLog_Level_2.addAction(self.actionDEBUG)
        self.menuLog_Level_2.addAction(self.actionVERBOSE)
        self.menuDeveloper.addAction(self.action_show_log_view)
        self.menuDeveloper.addAction(self.menuLog_Level_2.menuAction())
        self.menuBar.addAction(self.menuDeveloper.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fever Monitor"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.pushButton_stop.setText(_translate("MainWindow", "Stop"))
        self.label.setText(_translate("MainWindow", "FPS:"))
        self.label_fps.setText(_translate("MainWindow", "00.0"))
        self.pushButton_settings.setText(_translate("MainWindow", "Settings"))
        self.label_thermal_stream.setText(_translate("MainWindow", "Thermal Imaging Fever Monitor\n"
"with Face Detection\n"
"\n"
"Click \'Start\' to start the monitor."))
        self.menuDeveloper.setTitle(_translate("MainWindow", "Developer"))
        self.menuLog_Level_2.setTitle(_translate("MainWindow", "Log Level"))
        self.actionDISABLE2.setText(_translate("MainWindow", "DISABLE"))
        self.actionWARNING2.setText(_translate("MainWindow", "WARNING"))
        self.actionINFO2.setText(_translate("MainWindow", "INFO"))
        self.actionDEBUG2.setText(_translate("MainWindow", "DEBUG"))
        self.actionVERBOSE2.setText(_translate("MainWindow", "VERBOSE"))
        self.action_show_log_view.setText(_translate("MainWindow", "Show log view"))
        self.actionDISABLE.setText(_translate("MainWindow", "DISABLE"))
        self.actionWARNING.setText(_translate("MainWindow", "WARNING"))
        self.actionINFO.setText(_translate("MainWindow", "INFO"))
        self.actionDEBUG.setText(_translate("MainWindow", "DEBUG"))
        self.actionVERBOSE.setText(_translate("MainWindow", "VERBOSE"))
        self.actionShow_model_confidence_instead_of_face_temperature.setText(_translate("MainWindow", "Display confidence instead of temperature"))
