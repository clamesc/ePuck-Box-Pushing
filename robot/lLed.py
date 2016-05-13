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

import ldvbot
import lCommunication


class led_status:
    ON = 1
    OFF = 0
    
class led:
    '''
    led LDVbot
    '''


    def __init__(self, bot, ledID):
        """
        Constructor 
        
        :parameter: bot
        :pType: ldvbot.robot
        """
        if isinstance(bot, ldvbot.robot):
            self._status = led_status.OFF
            self._robot = bot
            self._ledID = ledID
            self._communication = lCommunication.communication(self._robot)
        else:
            logging.error('Parameter has to be of type robot')
            raise ValueError("Parameter has to be of type robot")        
  
    def setLED(self, status):
        """
        Setter led LDVbot
        
        :param    status: On/Off 
        :type    status: Integer
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if not 1 <= self._ledID < 4:
            logging.error('Invalid parameter for "led_num"! (1-3 expected)')
            raise ValueError('Invalid parameter for "led_num"! (1-3 expected)')
        if (status != led_status.OFF) and (status != led_status.ON):
            logging.error('Invalid parameter for "status"! (Invalid status [on/off expected])')
            raise ValueError('Invalid parameter for "status"! (Invalid status [on/off expected])')
        order = [self._robot.getRNumber(), 5, 2, self._ledID, status]
        
        i = 0
        while self._communication.send(order) == 'fail':
            if i > 4:
                logging.warn('NRF-transmission failed')
                return 'fail'
            i = i + 1
        
        if status == led_status.ON:    
            self._status = led_status.ON
        else:
            self._status = led_status.OFF
