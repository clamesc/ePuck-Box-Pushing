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

import eCommunication
import epuck


class movement:
    '''
    motor ePuck
    '''
    def __init__(self, bot):
        """
        Constructor 
        
        :parameter: bot
        :pType: epuck.robot
        """
        if isinstance(bot, epuck.robot):
            self._robot = bot
            self._communication = eCommunication.communication(self._robot)
            
        else:
            logging.error('Parameter has to be of type robot')
            raise ValueError("Parameter has to be of type robot") 
        
                 
    def setPosition(self, l_wheel, r_wheel):
        """
        Setter motor position
        maybe broken 
        
        :parameter: l_wheel, r_wheel
        :pType: integer
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if isinstance(l_wheel, int) and isinstance(r_wheel, int):
            order = ("P", l_wheel, r_wheel)
            self._communication.write_actuators_epuck(order)
        else:
            logging.error('ERROR: Invalid parameter for position (Integer expected)')  
            raise ValueError('ERROR: Invalid parameter for position (Integer expected)')
        
    def getPosition(self):    
        """
        Getter motor position 
        
        :return: motor position
        :rType: tuple (0, 0)
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        parameters = ('Q', 4, '@HH')
        response = self._communication.send_binary_mode_epuck(parameters)
        if type(response) is tuple and type(response[0]) is int:
            logging.debug(response)
            return response
        else: 
            logging.warn('WARNING: Wrong return value')
            return False 
                    
    def setSpeed(self, l_motor, r_motor):
        """
        Setter motor speed 
        
        :parameter: l_motor, r_motor
        :pType: integer
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if isinstance(l_motor, int) and isinstance(r_motor, int):
            order = ("D", int(l_motor), int(r_motor))
            self._communication.write_actuators_epuck(order)
        else:
            logging.error('ERROR: Invalid parameter for speed (Integer expected)')  
            raise ValueError('ERROR: Invalid parameter for speed (Integer expected)') 
        
    
    def getSpeed(self): 
        """
        Getter motor speed 
        
        :return: motor speed
        :rType: tuple (0, 0)
        """  
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        parameters = ('E', 4, '@HH')
        response = self._communication.send_binary_mode_epuck(parameters)
        if type(response) is tuple and type(response[0]) is int:
            logging.debug(response)
            return response
        else: 
            logging.warn('WARNING: Wrong return value')
            return False
        
    def drive_forward(self, speed):
        """
        drive forward method
        sets speed equally to both left and right motor 
        
        :parameter: speed
        :pType: integer
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        self.setSpeed(speed, speed)
        
    def stop(self):
        """
        set motor speed to (0, 0)
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        self._setSpeed_epuck(0, 0)
        