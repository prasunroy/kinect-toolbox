# -*- coding: utf-8 -*-
"""
Interface for Kinect sensor.
Created on Sat May  5 10:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/kinect-toolbox

"""


# imports
from __future__ import division
from __future__ import print_function

import ctypes
import numpy
import pygame
import sys

from pykinect2 import PyKinectRuntime
from pykinect2 import PyKinectV2


# KinectRuntime class
class KinectRuntime(object):
    
    # ~~~~~~~~ constructor ~~~~~~~~
    def __init__(self):
        # debug state
        self._debug = False
        
        # initialize pygame
        flag0, flag1 = pygame.init()
        if flag0:
            if self._debug: print('[DEBUG] PyGame initialized')
        else:
            if self._debug: print('[DEBUG] PyGame initialization failed')
            sys.exit(0)
        
        # create kinect runtime object
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color|\
                                                       PyKinectV2.FrameSourceTypes_Infrared|\
                                                       PyKinectV2.FrameSourceTypes_LongExposureInfrared|\
                                                       PyKinectV2.FrameSourceTypes_Depth|\
                                                       PyKinectV2.FrameSourceTypes_BodyIndex|\
                                                       PyKinectV2.FrameSourceTypes_Body|\
                                                       PyKinectV2.FrameSourceTypes_Audio)
        
        # frame dimensions
        self._colorFrame_W = self._kinect.color_frame_desc.Width
        self._colorFrame_H = self._kinect.color_frame_desc.Height
        self._depthFrame_W = self._kinect.depth_frame_desc.Width
        self._depthFrame_H = self._kinect.depth_frame_desc.Height
        
        # back buffer surface for getting kinect color frames
        self._frameSurface = pygame.Surface((self._colorFrame_W, self._colorFrame_H), 0, 32)
        
        # aspect ratio of back buffer surface
        self._aspect_ratio_w_h = self._frameSurface.get_width() / self._frameSurface.get_height()
        self._aspect_ratio_h_w = self._frameSurface.get_height() / self._frameSurface.get_width()
        
        # dimension of returned frame
        self._targetW = None
        self._targetH = None
        
        # detected frames
        self._colorFrame = None
        self._depthFrame = None
        self._bodyFrame = None
        
        # data acquisition
        self._kinectDump = False
        self._kinectFile = 'temp.txt'
        self._kinectData = []
        
        # control surface refresh rate
        self._fps = 60
        self._clock = pygame.time.Clock()
        
        return
    
    # ~~~~~~~~ draw bone ~~~~~~~~
    def _draw_bone(self, joints, jointPoints, joint0, joint1, color):
#        # tracking states of both joints
#        joint0State = joints[joint0].TrackingState
#        joint1State = joints[joint1].TrackingState
#        
#        # tracking failure
#        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked):
#            return
#        
#        # both joints are inferred
#        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
#            return
        
        # draw bone
        point0 = (jointPoints[joint0].x, jointPoints[joint0].y)
        point1 = (jointPoints[joint1].x, jointPoints[joint1].y)
        
        try:
            pygame.draw.line(self._frameSurface, color, point0, point1, 15)
            pygame.draw.rect(self._frameSurface, (0, 255, 0), (int(point0[0])-5, int(point0[1])-5, 10, 10), 0)
            pygame.draw.rect(self._frameSurface, (0, 255, 0), (int(point1[0])-5, int(point1[1])-5, 10, 10), 0)
        except:
            if self._debug: print('[DEBUG] PyGame drawing failed')
        
        return
    
    # ~~~~~~~~ draw body ~~~~~~~~
    def _draw_body(self, joints, jointPoints, color):
        # draw torso
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight, color)
        
        # draw left arm
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft, color)
        
        # draw right arm
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight, color)
        
        # draw left leg
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft, color)
        
        # draw right leg
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight, color)
        self._draw_bone(joints, jointPoints, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight, color)
        
        return
    
    # ~~~~~~~~ draw color frame ~~~~~~~~
    def _draw_color_frame(self, frame, surface):
        surface.lock()
        address = self._kinect.surface_as_array(surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        surface.unlock()
        
        return
    
    # ~~~~~~~~ set target frame dimension ~~~~~~~~
    def setFrameSize(self, size=(None, None)):
        self._targetW, self._targetH = size
        
        return
    
    # ~~~~~~~~ get frame from device ~~~~~~~~
    def getFrame(self):
        # received a color frame
        if self._kinect.has_new_color_frame():
            self._colorFrame = self._kinect.get_last_color_frame()
            self._draw_color_frame(self._colorFrame, self._frameSurface)
        
        # received a depth frame
        if self._kinect.has_new_depth_frame():
            self._depthFrame = self._kinect.get_last_depth_frame()
            self._depthFrame = self._depthFrame.reshape(self._depthFrame_H, self._depthFrame_W)
        
        # recceived a body frame
        if self._kinect.has_new_body_frame():
            self._bodyFrame = self._kinect.get_last_body_frame()
        
        # detected body
        if self._bodyFrame is not None:
            for i in range(self._kinect.max_body_count):
                body = self._bodyFrame.bodies[i]
                if not body.is_tracked:
                    continue
                joints = body.joints
                jointPoints = self._kinect.body_joints_to_color_space(joints)
                self._draw_body(joints, jointPoints, (255, 100, 100))
                depthPoints = self._kinect.body_joints_to_depth_space(joints)
                coordinates = []
                for j in range(len(depthPoints)):
                    x = int(max(min(depthPoints[j].x, 1e6), -1e6))
                    y = int(max(min(depthPoints[j].y, 1e6), -1e6))
                    if x < 0 or x >= self._depthFrame_W or y < 0 or y >= self._depthFrame_H:
                        coordinates = []
                        break
                    z = self._depthFrame[y, x]
                    coordinates.append(x)
                    coordinates.append(y)
                    coordinates.append(z)
                if len(coordinates) > 0 and self._kinectDump:
                    self._kinectData.append(coordinates)
                if len(self._kinectData) > 0 and not self._kinectDump:
                    data = numpy.asarray(self._kinectData, dtype='int')
                    numpy.savetxt(self._kinectFile, data, fmt='%d')
                    self._kinectData = []
        
        # copy back buffer surface to window preserving aspect ratio
        if self._targetW is None and self._targetH is None:
            targetW = self._frameSurface.get_width()
            targetH = self._frameSurface.get_height()
        elif self._targetW is None:
            targetH = self._targetH
            targetW = int(self._aspect_ratio_w_h * targetH)
        elif self._targetH is None:
            targetW = self._targetW
            targetH = int(self._aspect_ratio_h_w * targetW)
        else:
            targetW = self._targetW
            targetH = self._targetH
        target_surface = pygame.transform.scale(self._frameSurface, (targetW, targetH))
        
        # convert pygame surface to numpy array
        frame = pygame.surfarray.array3d(target_surface)
        
        # limit frames per second
        self._clock.tick(self._fps)
        
        return frame
    
    # ~~~~~~~~ clean up and release resources ~~~~~~~~
    def clear(self):
        self._kinect.close()
        pygame.quit()
        
        return
