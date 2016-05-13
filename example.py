#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    Copyright © 2016 by Michael Keil
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from robot.robot import robot
from robot.eLed import led_status
import time
import sys

def test_lConnect():
    mRobot = robot().getLdvBot(238)
    rRobot = robot().getLdvBot(237)
    rRobot.getInfrared().setReceiveMode()
    mRobot.connect()
    mRobot.getInfrared().getID()
    #time.sleep(1)
    #mRobot.getMotor().drive(100, 3000, 0)
    mRobot.disconnect()
    
def test_eConnect():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.disconnect()
    
def test_eLED(ledID):
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getLED(ledID).setLED(led_status.ON)
    mRobot.getLED(2).setLED(led_status.ON)
    mRobot.getLED(3).setLED(led_status.ON)
    mRobot.getLED(4).setLED(led_status.ON)
    mRobot.getLED(5).setLED(led_status.ON)
    mRobot.getLED(6).setLED(led_status.ON)
    mRobot.getLED(7).setLED(led_status.ON)
    mRobot.getLED(8).setLED(led_status.ON)   
    mRobot.getLED(9).setLED(led_status.ON)
    i=0
    while i < 2000000:
        i=i+1
    mRobot.reset()
    mRobot.disconnect()
    
def test_eAccelerometer():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getAccelerometer().getValues()
    mRobot.getAccelerometer().setAccelerometerFiltered(True)
    mRobot.getAccelerometer().getValues()
    i=0
    while i < 2000000:
        i=i+1
    mRobot.reset()
    mRobot.disconnect()
        
def test_eFirmware():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getFirmware().getVersion()
    mRobot.reset()
    mRobot.disconnect()
    
def test_eFloorsensor():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getFloorSensor().getValues()
    i=0
    while i < 25:
        mRobot.getFloorSensor().getValues()
        i=i+1
    mRobot.reset()
    mRobot.disconnect()    

def test_eMicrophone():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getMicrophone().getValues()
    i=0
    while i < 25:
        mRobot.getMicrophone().getValues()
        i=i+1 
    mRobot.reset()
    mRobot.disconnect()   
    
def test_eProximity():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getProximitySensor().calibrate()
    i=0
    while i < 25:
        mRobot.getProximitySensor().getValues()
        i=i+1 
    mRobot.reset()
    mRobot.disconnect() 
    
def test_eSelector(): 
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getSelector().getValues()
    i=0
    while i < 25:
        mRobot.getSelector().getValues()
        i=i+1 
    mRobot.reset()
    mRobot.disconnect() 
    
def test_eLightsensor():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getLightsensor().getValues()
    i=0
    while i < 25:
        mRobot.getLightsensor().getValues()
        i=i+1 
    mRobot.reset()
    mRobot.disconnect() 
    
def test_eMovement():
    mRobot = robot().getEpuck()
    mRobot.connect()
    mRobot.getMotor().getSpeed()
    mRobot.getMotor().getPosition()
    #mRobot.getMotor().setPosition(10, 10)
    mRobot.getMotor().setSpeed(200, 200)
    mRobot.getMotor().getSpeed()
    i=0
    while i < 200:
        mRobot.getMotor().getPosition()
        i=i+1 
    mRobot.reset()
    mRobot.disconnect() 
    
def test_eCamera():
    mRobot = robot().getEpuck()
    mRobot.connect()
    camera = mRobot.getCamera()
    camera.refresh_camera_parameters()
    camera.get_image()
    camera.save_image()
    camera.set_camera_parameters(0, 10, 10, 1)
    mRobot.reset()
    mRobot.disconnect() 
    
if __name__ == '__main__':
    try:
        test_eConnect()
        test_eMovement()
    except:
        mRobot = robot().getEpuck()
        mRobot.connect()
        mRobot.reset()
        mRobot.disconnect()
        sys.exit(0)
