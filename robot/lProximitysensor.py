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


class proximitysensor:
    
    '''
    proximity sensor LDVbot
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
        
    def getValues(self):
        """
        Getter proximity sensor 
        
        :return: proximity sensor values
        :rType: tuple [0, 0, 0, 0, 0, 0, 0, 0] all values in {0,1}
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        _rNumber = self._robot.getRNumber()
        order = [_rNumber, 4, 3, 1]
        response = self._communication.send_receive(order)
        i = 0
        while response == 'fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while int(response[0]) != _rNumber:
            response = self._communication.receive(order)
        if int(response[0]) == _rNumber:
            if response[2] != '102':
                data_response = lMisc.fail(response[2])
            else:
                data_response = lMisc.to_bin(response[3], 8)
        else:
            data_response = lMisc.fail(55)
        
        logging.debug(data_response)
        return data_response  
            
    def setSensitivity(self, sens):  # Set the threshold value for the distance sensors
        """
        Setter proximity sensor sensitivity
        
        :parameter: sens
        :pType: Integer [0,1023]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if not 0 <= sens <= 1023:
            raise ValueError('ERROR: Invalid parameter for "sens"! (0 - 1023 expected)')
        sens_tmp = struct.unpack('BB', struct.pack('H', sens))
        sens_int1 = sens_tmp[0]
        sens_int2 = sens_tmp[1]
        order = [self._robot.getRNumber(), 5, 201, sens_int1, sens_int2]
        logging.debug(order)
        i = 0
        while self._communication.send(order) == 'fail':
            if i > 4:
                return lMisc.fail(20)
            i = i + 1  
            
    def getSensitivity(self):  # Get the threshold value for the distance sensors
        """
        Getter proximity sensor sensitivity
        
        :return: sensitivity
        :rType: Integer [0,1023]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        _rNumber = self._robot.getRNumber()
        order = [_rNumber, 3, 207]
        response = self._communication.send_receive(order)
        i = 0
        while response == 'fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while int(response[0]) != _rNumber:
            response = self._communication.receive(order)
        if int(response[0]) == _rNumber:
            if response[2] != '108':
                data_response = lMisc.fail(response[2])
            else:
                data_response = (int(response[4]) << 8) + int(response[3])
        else:
            data_response = lMisc.fail(55)
        
        logging.debug(data_response)
        return data_response   