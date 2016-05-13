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

import eAccelerometer
import eCamera
import eCommunication
import eFirmware
import eFloorsensor 
import eLed 
import eLightsensor 
import eMicrophone 
import eMovement 
import eProximitysensor 
import eSelector 


class robot:
    '''
    ePuck Class
    '''    
    
    def __init__(self):
        """
        Constructor 
        """
        self._port = None
        self._connectionStatus = False
        self._communication = eCommunication.communication(self)

        self._movement = eMovement.movement(self)
        self._proximity =  eProximitysensor.proximitysensor(self)
        self._floor = eFloorsensor.floorsensor(self)
        self._led1 = eLed.led(self, 1)
        self._led2 = eLed.led(self, 2)
        self._led3 = eLed.led(self, 3)
        self._led4 = eLed.led(self, 4)
        self._led5 = eLed.led(self, 5)
        self._led6 = eLed.led(self, 6)
        self._led7 = eLed.led(self, 7)
        self._led8 = eLed.led(self, 8)
        self._led9 = eLed.led(self, 9)
        self._accelerometer = eAccelerometer.accelerometer(self)
        self._camera = eCamera.camera(self)
        self._firmware = eFirmware.firmwareVersion(self)
        self._lightsensor = eLightsensor.lightsensor(self)
        self._microphone = eMicrophone.microphone(self)
        self._selector = eSelector.selector(self)
  
        
    

    def getMotor(self):
        """
        Getter Motor
        
        :return: movement
        :rType: eMovement.motor
        """
        return self._movement
    
    def getFloorSensor(self):
        """
        Getter floor sensor
        
        :return: floor sensor
        :rType: eFloorsensor.floorsensor
        """
        return self._floor
     
    
    def getProximitySensor(self):
        """
        Getter proximity sensor
        
        :return: proximity sensor
        :_rType: eProximitysensor.proximitysensor
        """
        return self._proximity
        
    
    
    def getLED(self, ledID):
        """
        Getter LED
        
        :parameter ledID
        :pType integer
        :return: led
        :rType: eLed.led
        """
        if ledID == 1:
            return self._led1
        elif ledID == 2:
            return self._led2
        elif ledID == 3:
            return self._led3
        elif ledID == 4:
            return self._led4
        elif ledID == 5:
            return self._led5
        elif ledID == 6:
            return self._led6
        elif ledID == 7:
            return self._led7
        elif ledID == 8:
            return self._led8
        elif ledID == 9:
            return self._led9
        else:
            logging.error('ERROR: ledID has to be in [1,9]')  
            raise ValueError('ERROR: ledID has to be in [1,9]')  
    
    def getAccelerometer(self):
        """
        Getter Accelerometer
        
        :return: accelerometer
        :rType: eAccelerometer.accelerometer
        """
        return self._accelerometer
    
    def getCamera(self):
        """
        Getter Camera
        
        :return: camera
        :rType: eCamera.camera
        """
        return self._camera
        
    def getFirmware(self):
        """
        Getter Firmware
        
        :return: firmware
        :rType: eFirmware.firmware
        """
        return self._firmware  
        
    def getLightsensor(self):
        """
        Getter light sensor
        
        :return: light sensor
        :rType: eLightsensor.lightsensor
        """
        return self._lightsensor
        
    def getMicrophone(self):
        """
        Getter Microphone
        
        :return: microphone
        :rType: eMicrophone.microphone
        """
        return self._microphone              
        
    
    def getSelector(self):
        """
        Getter Selector
        
        :return: selector
        :rType: eSelector.selector
        """
        return self._selector              
                
                
    def getConnectionStatus(self):
        """
        Getter connectionStatus
        
        :return: _connectionStatus
        :rType: boolean
        """
        return self._connectionStatus
    
    def getPort(self):
        """
        Getter _port
        
        :return: _port
        :Type: Port
        """
        return self._port
             
    def disconnect(self):
        """
        Disconnect from robot
        
        :return: If disconnect was successful
        :rType: boolean
        :raise Exception: if it was a problem closing the connection
        """
        if self._connectionStatus:
            try:
                self.stop()
                self._port.close()
                self._connectionStatus = False
                logging.info('disconnected')
                return True
            except Exception, e:
                logging.exception('Connection close problem: \n' + str(e))
                raise Exception, 'Connection close problem: \n' + str(e)    
            
        else:
            return False
        
    def isConnected(self):
        """
        Getter connection status
        """
        return self._connectionStatus    

               
    def reset(self):
        """
        Reset the robot
        
        :return: Successful operation
        :rType: boolean
        :raise Exception: If there is not connection
        """
        if not self._connectionStatus:
            logging.exception('No connection available')
            raise Exception, 'No connection available'

        respond = self._communication.send_receive("R")
        logging.debug('Reset respond: ' + respond)

        return True
                
    def stop(self):
        """
        Stop the motor and turn off all leds
        :return: Successful operation
        :rType: boolean
        :raise Exception: If there is not connection
        """

        if not self._connectionStatus:
            logging.exception('No connection available')
            raise Exception, 'No connection available'

        respond = self._communication.send_receive("S")
        logging.debug(respond)

        if respond == "s":
            return True
        else:
            return False      
        
    def connect(self):
        """
        Connect with the physical ePuck
        
        :return: If the connection was successful
        :rType: Boolean
        :except Exception: If there are a communication problem, for example, the robot is off
        """
        try:
            self._port = serial.Serial()
            self._port.baudrate = 230400
            self._port.port = '/dev/ttyS0'
            self._port.timeout = 0.05
            self._port.open()
            
            self._connectionStatus = True
            logging.info('Connected')
            self.reset()
            
        except Exception, e:  
            logging.exception('Connection problem: \n' + str(e))
            raise Exception, 'Connection problem: \n' + str(e)
