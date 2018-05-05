# -*- coding: utf-8 -*-
"""
Visualization of Kinect body joints data in 3D.
Created on Sat May  5 14:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/kinect-toolbox

"""


# imports
from mpl_toolkits.mplot3d import Axes3D
from pykinect2 import PyKinectV2
from PyQt5.QtCore import QTimer


# QtPlot class
class QtPlot(object):
    
    # ~~~~~~~~ constructor ~~~~~~~~
    def __init__(self, figure, canvas):
        # joint data
        self.data = None
        self.dataHead = -1
        self.dataTail = -1
        
        # joint connections for Kinect v1
        self.connections = [[PyKinectV2.JointType_Head,
                             PyKinectV2.JointType_Neck],
                            [PyKinectV2.JointType_Neck,
                             PyKinectV2.JointType_SpineMid],
                            [PyKinectV2.JointType_SpineMid,
                             PyKinectV2.JointType_SpineBase],
                            [PyKinectV2.JointType_Neck,
                             PyKinectV2.JointType_ShoulderLeft],
                            [PyKinectV2.JointType_Neck,
                             PyKinectV2.JointType_ShoulderRight],
                            [PyKinectV2.JointType_SpineBase,
                             PyKinectV2.JointType_HipLeft],
                            [PyKinectV2.JointType_SpineBase,
                             PyKinectV2.JointType_HipRight],
                            [PyKinectV2.JointType_ShoulderLeft,
                             PyKinectV2.JointType_ElbowLeft],
                            [PyKinectV2.JointType_ElbowLeft,
                             PyKinectV2.JointType_WristLeft],
                            [PyKinectV2.JointType_WristLeft,
                             PyKinectV2.JointType_HandLeft],
                            [PyKinectV2.JointType_ShoulderRight,
                             PyKinectV2.JointType_ElbowRight],
                            [PyKinectV2.JointType_ElbowRight,
                             PyKinectV2.JointType_WristRight],
                            [PyKinectV2.JointType_WristRight,
                             PyKinectV2.JointType_HandRight],
                            [PyKinectV2.JointType_HipLeft,
                             PyKinectV2.JointType_KneeLeft],
                            [PyKinectV2.JointType_KneeLeft,
                             PyKinectV2.JointType_AnkleLeft],
                            [PyKinectV2.JointType_AnkleLeft,
                             PyKinectV2.JointType_FootLeft],
                            [PyKinectV2.JointType_HipRight,
                             PyKinectV2.JointType_KneeRight],
                            [PyKinectV2.JointType_KneeRight,
                             PyKinectV2.JointType_AnkleRight],
                            [PyKinectV2.JointType_AnkleRight,
                             PyKinectV2.JointType_FootRight]]
        
        # joint connections for Kinect v2
        self.connections2 = [[PyKinectV2.JointType_Head,
                              PyKinectV2.JointType_Neck],
                             [PyKinectV2.JointType_Neck,
                              PyKinectV2.JointType_SpineShoulder],
                             [PyKinectV2.JointType_SpineShoulder,
                              PyKinectV2.JointType_SpineMid],
                             [PyKinectV2.JointType_SpineMid,
                              PyKinectV2.JointType_SpineBase],
                             [PyKinectV2.JointType_SpineShoulder,
                              PyKinectV2.JointType_ShoulderLeft],
                             [PyKinectV2.JointType_SpineShoulder,
                              PyKinectV2.JointType_ShoulderRight],
                             [PyKinectV2.JointType_SpineBase,
                              PyKinectV2.JointType_HipLeft],
                             [PyKinectV2.JointType_SpineBase,
                              PyKinectV2.JointType_HipRight],
                             [PyKinectV2.JointType_ShoulderLeft,
                              PyKinectV2.JointType_ElbowLeft],
                             [PyKinectV2.JointType_ElbowLeft,
                              PyKinectV2.JointType_WristLeft],
                             [PyKinectV2.JointType_WristLeft,
                              PyKinectV2.JointType_HandLeft],
                             [PyKinectV2.JointType_HandLeft,
                              PyKinectV2.JointType_HandTipLeft],
                             [PyKinectV2.JointType_WristLeft,
                              PyKinectV2.JointType_ThumbLeft],
                             [PyKinectV2.JointType_ShoulderRight,
                              PyKinectV2.JointType_ElbowRight],
                             [PyKinectV2.JointType_ElbowRight,
                              PyKinectV2.JointType_WristRight],
                             [PyKinectV2.JointType_WristRight,
                              PyKinectV2.JointType_HandRight],
                             [PyKinectV2.JointType_HandRight,
                              PyKinectV2.JointType_HandTipRight],
                             [PyKinectV2.JointType_WristRight,
                              PyKinectV2.JointType_ThumbRight],
                             [PyKinectV2.JointType_HipLeft,
                              PyKinectV2.JointType_KneeLeft],
                             [PyKinectV2.JointType_KneeLeft,
                              PyKinectV2.JointType_AnkleLeft],
                             [PyKinectV2.JointType_AnkleLeft,
                              PyKinectV2.JointType_FootLeft],
                             [PyKinectV2.JointType_HipRight,
                              PyKinectV2.JointType_KneeRight],
                             [PyKinectV2.JointType_KneeRight,
                              PyKinectV2.JointType_AnkleRight],
                             [PyKinectV2.JointType_AnkleRight,
                              PyKinectV2.JointType_FootRight]]
        
        # figure and canvas for plotting
        self.figure = figure
        self.canvas = canvas
        
        # update timer
        self.timer = None
        
        return
    
    # ~~~~~~~~ clear ~~~~~~~~
    def clear(self):
        self.data = None
        self.dataHead = -1
        self.dataTail = -1
        self.figure.clear()
        self.canvas.draw()
        if self.timer is not None:
            self.timer.stop()
        
        return
    
    # ~~~~~~~~ plot ~~~~~~~~
    def plot(self, data):
        self.clear()
        self.data = data
        self.dataHead = 0
        self.dataTail = self.data.shape[0] - 1
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_plot)
        self.timer.start(100)
        
        return
    
    # ~~~~~~~~ update plot ~~~~~~~~
    def _update_plot(self):
        try:
            joints = self.data[self.dataHead].reshape(-1, 3)
            x = joints[:, 0]
            y = joints[:, 1]
            z = joints[:, 2]
            self.figure.clear()
            axes = self.figure.gca(projection=Axes3D.name)
            axes.set_facecolor('none')
            axes.set_xlim([-1, 1])
            axes.set_ylim([-1, 1])
            axes.set_zlim([-1, 1])
            # axes.set_xlabel('X-axis')
            # axes.set_ylabel('Z-axis')
            # axes.set_zlabel('Y-axis')
            axes.set_xticklabels([])
            axes.set_yticklabels([])
            axes.set_zticklabels([])
            axes.invert_xaxis()
            axes.set_title('FRAME {:3d} / {:3d}'
                           .format(self.dataHead+1, self.dataTail+1))
            axes.scatter(x, z, y, c='#64a0ff')
            if len(joints) == 20:
                connections = self.connections
            elif len(joints) == 25:
                connections = self.connections2
            else:
                connections = []
            for connection in connections:
                axes.plot(x[connection], z[connection], y[connection],
                          c='#ff6464')
            self.canvas.draw()
            self.dataHead += 1
            if self.dataHead > self.dataTail:
                self.dataHead  = 0
        except:
            pass
        
        return
