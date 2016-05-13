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

import epuck
import eCommunication


class selector:
    '''
    Selector ePuck
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
        
    def getValues(self):
        """
        Getter selector values 
        
        :return: selector values
        :pType: string
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        response = self._communication.send_receive('c').split(",")
        t = response[0]
        response = tuple(response[1:len(response)])

        if t == "c":
            # Selector
            logging.debug(response)
            return response[0]
        else: 
            logging.warn('WARNING: Wrong return value')
            return False 