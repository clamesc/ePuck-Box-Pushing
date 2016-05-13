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
import logging

import serial
import time

import lAnalog 
import lBattery 
import lBotID 
import lCommunication 
import lFloorsensor 
import lInfrared
import lLed 
import lMovement 
import lProximitysensor


class robot:
    '''
    LDVbot
    '''    
    
    def __init__(self, rNumber=None):
        """
        Constructor 
        
        :parameter: bot
        :pType: ldvbot.robot
        """
        self._rNumber = None
        self._port = None
        self._connectionStatus = False
        self._communication = lCommunication.communication(self)
        
        if rNumber == None:
            logging.exception('Parameter rNumber for LDVbot is missing')
            raise ValueError('Parameter rNumber for LDVbot is missing')
        else:
            self._rNumber = rNumber
                
        
        self._movement = lMovement.movement(self)
        self._proximity =  lProximitysensor.proximitysensor(self)
        self._floor = lFloorsensor.floorsensor(self)
        self._led1 = lLed.led(self, 1)
        self._led2 = lLed.led(self, 2)
        self._led3 = lLed.led(self, 3)
        self._battery = lBattery.battery(self)
        self._botID = lBotID.robotID(self)
        self._infrared = lInfrared.infrared(self)
        self._analog = lAnalog.analog(self)                         
        
       
    

    def getMotor(self):
        """
        Getter Motor
        
        :return: movement
        :_rType: _motor._motor
        """
        return self._movement
    
    def getFloorSensor(self):
        """
        Getter FloorSensor
        
        :return: _floorSensor
        :_rType: floorsensor.floorsensor
        """
        return self._floor
     
    
    def getProximitySensor(self):
        """
        Getter ProximitySensor
        
        :return: _proximitySensor
        :_rType: proximitySensor.proximitySensor
        """
        return self._proximity
    
    
    def getLED(self, ledID):
        """
        Getter LED
        
        :return: _led
        :_rType: Tuple
        :_rType_tuple: led.led
        """
        if ledID == 1:
            return self._led1
        elif ledID == 2:
            return self._led2
        elif ledID == 3:
            return self._led3
        else:
            logging.error('ERROR: ledID has to be in [1,3]')  
            raise ValueError('ERROR: ledID has to be in [1,3]') 
        
    def getBattery(self):
        """
        Getter Battery
        
        :return: _battery
        :_rType: battery.battery
        """
        return self._battery
        
    def getRobotID(self):
        """
        Getter RobotID
        
        :return: _botID
        :_rType: botID.robotID
        """
        return self._botID        
        
    
    def getInfrared(self):
        """
        Getter Infrared
        
        :return: _infrared
        :_rType: infrared.infrared
        """
        return self._infrared
        
    def getAnalog(self):
        """
        Getter Analog (analog read and write methods of LDVbot and destroy)
        
        :return: _ldvbot
        :_rType: analog.analog
        """
        return self._analog
            
    def getRNumber(self):
        """
        Getter rNumber
        
        :return: _rNumber
        :_rType: integer
        """
        return self._rNumber 
    
    def getConnectionStatus(self):
        """
        Getter _connectionStatus
        
        :return: _connectionStatus
        :_rType: Boolean
        """
        return self._connectionStatus
    
    def getPort(self):
        """
        Getter _port
        
        :return: _port
        :_rType: Port
        """
        return self._port
         
    
    def disconnect(self):
        """
        Disconnect from robot
        
        :return: If disconnect was successful
        :_rType: Boolean
        :raise Exception: if it was a problem closing the connection
        """
        if self._connectionStatus:
            try:
                self.stop()
                self._port.close()
                self._connectionStatus = False
                logging.info('disconnected')
            except Exception, e:
                logging.exception('Connection close problem: \n' + str(e))
                raise Exception, 'Connection close problem: \n' + str(e)    
            
        else:
            return False
        
    def isConnected(self):
        """
        get connection status
        """
        return self._connectionStatus    
        
    def stop(self):
        """
        Stop the motor and turn off all leds
        :return: Successful operation
        :_rType: Boolean
        """            
        
        if not self._connectionStatus:
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        self.getMotor().stop()
        time.sleep(1)
        self.getLED(1).setLED(0)
        time.sleep(1)
        self.getLED(2).setLED(0)
        time.sleep(1)
        self.getLED(3).setLED(0)
                 
    def connect(self, mPort='/dev/ttyACM0'):
        """
        Connect with the physical analog
        
        :return: If the connection was successful
        :_rType: Boolean
        :except Exception: If there are a communication problem, for example, the robot is off
        """
        try:
            self._port = serial.Serial()
            self._port.baudrate = 57600
            self._port.port = mPort
            self._port.stopbits = serial.STOPBITS_ONE
            self._port.parity = serial.PARITY_NONE
            self._port.timeout = None
            self._port.open()  
            
            self._connectionStatus = True
            logging.info('Connected')
        except Exception, e:  
            logging.exception('Connection problem: \n' + str(e))
            raise Exception, 'Connection problem: \n' + str(e)       
