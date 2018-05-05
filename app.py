# -*- coding: utf-8 -*-
"""
Kinect data acquisition and visualization toolbox.
Created on Sat May  5 17:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/kinect-toolbox

"""


# imports
from __future__ import division
from __future__ import print_function

import numpy
import os
import pandas
import random
import sys
import webbrowser

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QImage, QMovie, QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QWidget
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFileDialog
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from kinect import KinectRuntime
from qtplot import QtPlot


# MainGUI class
class MainGUI(QWidget):
    
    # ~~~~~~~~ constructor ~~~~~~~~
    def __init__(self):
        super().__init__()
        self.init_UI()
        
        return
    
    # ~~~~~~~~ initialize ui ~~~~~~~~
    def init_UI(self):
        # set properties
        self.setGeometry(0, 0, 0, 0)
        self.setStyleSheet('QWidget {background-color: #ffffff;}')
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.setWindowTitle('Kinect Data Acquisition and Visualization Toolbox')
        
        # create widgets
        # -- connect device button --
        self.btn_conn = QPushButton('Connect Device')
        self.btn_conn.setMinimumHeight(40)
        self.btn_conn_style_0 = 'QPushButton {background-color: #00a86c; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        self.btn_conn_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        self.btn_conn.setStyleSheet(self.btn_conn_style_0)
        
        # -- select directory textbox --
        self.filepath = QLineEdit()
        self.filepath.setMinimumSize(250, 30)
        self.filepath.setReadOnly(True)
        self.filepath.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.filepath.setPlaceholderText(os.getcwd())
        
        # -- select directory button --
        self.btn_path = QPushButton('Select Directory')
        self.btn_path.setMinimumSize(150, 30)
        self.btn_path_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_path_style_1 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_path.setStyleSheet(self.btn_path_style_0)
        
        # -- control recording textbox --
        self.filename = QLineEdit()
        self.filename.setMinimumSize(250, 30)
        self.filename.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.filename.setPlaceholderText('Enter filename...')
        
        # -- control recording button --
        self.btn_recd = QPushButton('Start Recording')
        self.btn_recd.setMinimumSize(150, 30)
        self.btn_recd_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_recd_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_recd.setStyleSheet(self.btn_recd_style_0)
        
        # -- control plot textbox --
        self.plotfile = QLineEdit()
        self.plotfile.setMinimumSize(250, 30)
        self.plotfile.setReadOnly(True)
        self.plotfile.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.plotfile.setPlaceholderText(os.path.join(os.getcwd(), 'temp.txt'))
        
        # -- control plot button --
        self.btn_plot = QPushButton('Import Kinect Data')
        self.btn_plot.setMinimumSize(150, 30)
        self.btn_plot_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_plot_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_plot.setStyleSheet(self.btn_plot_style_0)
        
        # -- camera feed --
        self.cam_feed = QLabel()
        self.cam_feed.setMinimumSize(640, 360)
        self.cam_feed.setAlignment(Qt.AlignCenter)
        self.cam_feed.setFrameStyle(QFrame.StyledPanel)
        self.cam_feed.setStyleSheet('QLabel {background-color: #000000;}')
        
        # -- plot area --
        self.figure = pyplot.figure()
        self.figure.set_facecolor('#f5f5f5')
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumSize(640, 360)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        # -- animation --
        self.movie = QMovie('assets/anim.gif')
        self.animation = QLabel()
        self.animation.setMinimumWidth(500)
        self.animation.setAlignment(Qt.AlignCenter)
        self.animation.setStyleSheet('QLabel {background-color: #ffffff;}')
        self.animation.setMovie(self.movie)
        self.movie.start()
        
        # -- control animation button --
        self.btn_anim = QPushButton()
        self.btn_anim.setFixedSize(20, 20)
        self.btn_anim.setStyleSheet('QPushButton {background-color: none; border: none;}')
        self.btn_anim.setIcon(QIcon('assets/button_anim.png'))
        self.btn_anim.setIconSize(QSize(20, 20))
        self.btn_anim.setToolTip('Toggle animation')
        
        # -- repository link button --
        self.btn_repo = QPushButton()
        self.btn_repo.setFixedSize(20, 20)
        self.btn_repo.setStyleSheet('QPushButton {background-color: none; border: none;}')
        self.btn_repo.setIcon(QIcon('assets/button_repo.png'))
        self.btn_repo.setIconSize(QSize(20, 20))
        self.btn_repo.setToolTip('Fork me on GitHub')
        
        # -- copyright --
        self.copyright = QLabel('\u00A9 2018 Indian Staistical Institute')
        self.copyright.setFixedHeight(20)
        self.copyright.setAlignment(Qt.AlignCenter)
        self.copyright.setStyleSheet('QLabel {background-color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}')
        
        # create layouts
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.btn_conn)
        
        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.filepath)
        h_box2.addWidget(self.btn_path)
        
        h_box3 = QHBoxLayout()
        h_box3.addWidget(self.filename)
        h_box3.addWidget(self.btn_recd)
        
        h_box4 = QHBoxLayout()
        h_box4.addWidget(self.plotfile)
        h_box4.addWidget(self.btn_plot)
        
        h_box5 = QHBoxLayout()
        h_box5.addWidget(self.animation)
        
        h_box6 = QHBoxLayout()
        h_box6.addWidget(self.btn_anim)
        h_box6.addWidget(self.copyright)
        h_box6.addWidget(self.btn_repo)
        
        v_box1 = QVBoxLayout()
        v_box1.addLayout(h_box1)
        v_box1.addLayout(h_box2)
        v_box1.addLayout(h_box3)
        v_box1.addLayout(h_box4)
        v_box1.addStretch()
        v_box1.addLayout(h_box5)
        v_box1.addLayout(h_box6)
        
        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.cam_feed)
        v_box2.addWidget(self.toolbar)
        v_box2.addWidget(self.canvas)
        
        g_box0 = QGridLayout()
        g_box0.addLayout(v_box1, 0, 0, -1, 2)
        g_box0.addLayout(v_box2, 0, 2, -1, 4)
        
        self.setLayout(g_box0)
        
        # create Plot
        self.qtplot = QtPlot(self.figure, self.canvas)
        
        # set slots for signals
        self.flg_conn = False
        self.flg_recd = False
        self.flg_plot = False
        self.flg_anim = True
        
        self.btn_conn.clicked.connect(self.connect)
        self.btn_path.clicked.connect(self.selectDirectory)
        self.btn_recd.clicked.connect(self.record)
        self.btn_plot.clicked.connect(self.plot)
        self.btn_anim.clicked.connect(self.toggleAnimation)
        self.btn_repo.clicked.connect(self.openRepository)
        
        return
    
    # ~~~~~~~~ window centering ~~~~~~~~
    def moveWindowToCenter(self):
        window_rect = self.frameGeometry()
        screen_cent = QDesktopWidget().availableGeometry().center()
        window_rect.moveCenter(screen_cent)
        self.move(window_rect.topLeft())
        
        return
    
    # ~~~~~~~~ connect device ~~~~~~~~
    def connect(self):
        if self.flg_recd:
            self.record()
        self.flg_conn = not self.flg_conn
        if self.flg_conn:
            self.btn_conn.setStyleSheet(self.btn_conn_style_1)
            self.btn_conn.setText('Disconnect Device')
            self.device = KinectRuntime()
            self.timer = QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(50)
        else:
            self.btn_conn.setStyleSheet(self.btn_conn_style_0)
            self.btn_conn.setText('Connect Device')
            self.cam_feed.clear()
            self.timer.stop()
            self.device.clear()
        
        return
    
    # ~~~~~~~~ update ~~~~~~~~
    def update(self):
        self.device.setFrameSize((None, self.cam_feed.height()))
        frame = self.device.getFrame()
        frame = numpy.transpose(frame, (1, 0, 2)).copy()
        frame = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.cam_feed.setPixmap(QPixmap.fromImage(frame))
        
        return
    
    # ~~~~~~~~ select directory ~~~~~~~~
    def selectDirectory(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if path:
            self.filepath.setText(os.path.normpath(path))
        
        return
    
    # ~~~~~~~~ record ~~~~~~~~
    def record(self):
        if not self.flg_conn:
            return
        
        self.flg_recd = not self.flg_recd
        self.device._kinectDump = self.flg_recd
        
        if self.flg_recd:
            if not self.filename.text():
                self.filename.setText('temp.txt')
            elif os.path.splitext(self.filename.text())[-1] != '.txt':
                self.filename.setText(''.join([self.filename.text(), '.txt']))
            
            fname, fextn = os.path.splitext(self.filename.text())
            absolutePath = os.path.join(self.filepath.text(), self.filename.text())
            
            while os.path.exists(absolutePath):
                hex8 = ''.join(['0123456789ABCDEF'[random.randint(0, 0xF)] for _ in range(8)])
                name = ''.join(['_'.join([fname, hex8]), fextn])
                absolutePath = os.path.join(self.filepath.text(), name)
            
            self.device._kinectFile = absolutePath
            self.btn_recd.setStyleSheet(self.btn_recd_style_1)
            self.btn_recd.setText('Stop Recording')
        else:
            self.btn_recd.setStyleSheet(self.btn_recd_style_0)
            self.btn_recd.setText('Start Recording')
        
        return
    
    # ~~~~~~~~ plot ~~~~~~~~
    def plot(self):
        self.flg_plot = not self.flg_plot
        if self.flg_plot:
            path = QFileDialog.getOpenFileName(self, 'Import Kinect Data', os.getenv('HOME'), 'Kinect Data (*.txt *.csv)')[0]
            if not path:
                self.flg_plot = not self.flg_plot
                return
            extn = os.path.splitext(path)[-1]
            if extn == '.txt':
                data = pandas.read_csv(path, sep=' ', header=None).values
            elif extn == '.csv':
                data = pandas.read_csv(path, sep=',', header=None).values
            self.plotfile.setText(os.path.normpath(path))
            self.btn_plot.setStyleSheet(self.btn_plot_style_1)
            self.btn_plot.setText('Clear Plot')
            self.qtplot.plot(data)
        else:
            self.btn_plot.setStyleSheet(self.btn_plot_style_0)
            self.btn_plot.setText('Import Kinect Data')
            self.plotfile.clear()
            self.qtplot.clear()
        
        return
    
    # ~~~~~~~~ toggle animation ~~~~~~~~
    def toggleAnimation(self):
        self.flg_anim = not self.flg_anim
        if self.flg_anim:
            self.animation.setMovie(self.movie)
            self.movie.start()
        else:
            self.movie.stop()
            self.animation.clear()
        
        return
    
    # ~~~~~~~~ open repository ~~~~~~~~
    def openRepository(self):
        webbrowser.open('https://github.com/prasunroy/kinect-toolbox')
        
        return
    
    # ~~~~~~~~ close event ~~~~~~~~
    def closeEvent(self, event):
        if self.flg_conn:
            self.connect()
        if self.flg_plot:
            self.qtplot.clear()
        if self.flg_anim:
            self.toggleAnimation()
        
        return


# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = MainGUI()
    gui.show()
    gui.moveWindowToCenter()
    sys.exit(app.exec_())
