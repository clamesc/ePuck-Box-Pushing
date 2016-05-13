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
import struct

import ldvbot
import lCommunication
import lMisc


class movement:
    '''
    motor LDVbot
    '''
    def __init__(self, bot):
        """
        Constructor 
        
        :parameter: bot
        :pType: ldvbot.robot
        """
        if isinstance(bot, ldvbot.robot):
            self._robot = bot
            self._communication = lCommunication.communication(self._robot)

        else:
            logging.error('Parameter has to be of type robot')
            raise ValueError("Parameter has to be of type robot") 
                
    def drive(self, speed, dist, angle): 
        """
        Setter Motor drive
        
        :parameter: speed
        :pType: Integer [-100,100]
        :parameter dist
        :pType: Integer [0,65500]
        :parameter: angle
        :pType: Intger [-360,360]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if not -100 <= speed <= 100:
            logging.error('ERROR: Invalid parameter for "speed"! (-100[backward] - 100[forward] expected)')
            raise ValueError('ERROR: Invalid parameter for "speed"! (-100[backward] - 100[forward] expected)')
        speed = speed + 100
        speed_tmp = struct.unpack('BB', struct.pack('H', speed))
        speed_int = speed_tmp[0]
        if not 0 <= dist < 65500:
            logging.error('ERROR: Invalid parameter for "distance"! (0mm - 65500mm expected)')
            raise ValueError('ERROR: Invalid parameter for "distance"! (0mm - 65500mm expected)')
        distance_tmp = struct.unpack('BB', struct.pack('H', dist))
        dist_int1 = distance_tmp[0]
        dist_int2 = distance_tmp[1]
        if not -360 <= angle <= 360:
            logging.error('ERROR: Invalid parameter for "angle"! (-360-360 degree expected)')
            raise ValueError('ERROR: Invalid parameter for "angle"! (-360-360 degree expected)')
        angle = angle + 360
        angle_tmp = struct.unpack('BB', struct.pack('H', angle))
        angle_int1 = angle_tmp[0]
        angle_int2 = angle_tmp[1]
        order = [self._robot.getRNumber(), 8, 1, speed_int, dist_int1, dist_int2, angle_int1, angle_int2]
        
        logging.debug(order)
        
        i = 0
        while self._communication.send(order) == 'fail':
            if i > 4:
                logging.warn('NRF-transmission failed')
                return 'fail'
            i = i + 1    
    
    def turnLeft(self):  # Turn the robot to the left side (90 degree)
        """
        Turn left 90 degree
        """
        if self.drive(90, 1, 83) == 'fail':
            return 'fail'


    def turnRight(self):  # Turn the robot to the right side (90 degree)
        """
        Turn right 90 degree 
        """
        if self.drive(90, 1, -83) == 'fail':
            return 'fail'
    
    
    def turnAround(self):  # Turn the robot around (180 degree)
        """
        Turn around 180 degree 
        """
        if self.drive(90, 1, -160) == 'fail':
            return 'fail' 
    
    def driveForward(self, speed):
        """
        Drive forward distance 65000, angle 0
        
        :parameter: speed
        :pType: Integer [-100,100] 
        """
        if self.drive(-speed, 65000, 0) == 'fail':        
            return 'fail'
        
    def stop(self):
        """
        Stop (drive(0,0,0))
        """
        if self.drive(0, 0, 0) == 'fail':
            return 'fail'   
        
    def isRunning(self):    
        """
        Check if is running
        
        :return: check if roboter is running
        :rType: Integer [0,1]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        order = [self._robot.getRNumber(), 3, 209]
        response = self._communication.send_receive(order)
        i = 0
        while response == 'fail':
            response = self._communication.send_receive(order)
            if i > 4:
                logging.warn('NRF-transmission failed')
                return 'fail'
            i = i + 1
            
        while int(response[0]) != self._robot.getRNumber():
            response = self._communication.receive()()
        if int(response[0]) == self._robot.getRNumber():
            if response[2] != '110':
                data_response = lMisc.fail(response[2])
            else:
                data_response = lMisc.to_bin(response[3], 1)
        else:
            data_response = lMisc.fail(55)
        
        logging.debug(data_response)
        return data_response