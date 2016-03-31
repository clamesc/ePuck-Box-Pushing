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
import lMisc


class analog:
    '''
    analog methods LDVbot
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
        
    def setdestroy(self, d1=0, d2=0, d3=0, d4=0, d5=0, d6=0, d7=0, d8=0, g1=0, g2=0, g3=0):
        """
        Setter destroy 
        
        :parameter: d1 (default=0), d2 (default=0), d3 (default=0), d4 (default=0),
        d5 (default=0), d6 (default=0), d7 (default=0), d8 (default=0),
        g1 (default=0), g2 (default=0), g3 (default=0),
        :pType: Integer
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        # Set certain sensors simulating a 'High' signal (ground and distance sensors)
        data_to_send1 = d8
        data_to_send1 = (int(data_to_send1) << 1) + int(d7)
        data_to_send1 = (int(data_to_send1) << 1) + int(d6)
        data_to_send1 = (int(data_to_send1) << 1) + int(d5)
        data_to_send1 = (int(data_to_send1) << 1) + int(d4)
        data_to_send1 = (int(data_to_send1) << 1) + int(d3)
        data_to_send1 = (int(data_to_send1) << 1) + int(d2)
        data_to_send1 = (int(data_to_send1) << 1) + int(d1)
        data_to_send2 = g3
        data_to_send2 = (int(data_to_send2) << 1) + int(g2)
        data_to_send2 = (int(data_to_send2) << 1) + int(g1)
        order = [self._robot.getRNumber(), 5, 202, data_to_send1, data_to_send2]
        logging.debug(order)
        i = 0
        while self._communication.send(order) == 'fail':
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
    
    
    def getdestroy(self):  # Check on what sensors a 'High' is simulated (ground and distance sensors)
        """
        Getter destroy 
        
        :return: response
        :rType: 
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        _rNumber = self._robot.getRNumber()
        order = [_rNumber, 3, 208]
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
            data_response = []
            if response[2] != '109':
                data_response = lMisc.fail(response[2])
            else:
                data_response.append(lMisc.to_bin(response[3], 8))
                data_response.append(lMisc.to_bin(response[4], 3))
        else:
            data_response = lMisc.fail(55)
            
        logging.debug(data_response)
        return data_response
    
    
    def analogread(self, sensor):  # Get the analog value of a specific sensor
        """
        Analog read 
        
        :parameter: sensor
        :pType: Integer
        :return: response
        :rType: 
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        _rNumber = self._robot.getRNumber()
        if (sensor <= 0) or (sensor >= 12):
            raise ValueError('ERROR: Invalid parameter for "sensor"! (1-11 expected)')
        order = [_rNumber, 4, 5, sensor]
        response = self._communication.send_receive(order)
        i = 0
        while (response == 'fail'):
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while int(response[0]) != _rNumber:
            response = self._communication.receive(order)
        if int(response[0]) == _rNumber:
            if response[2] != '100':
                data_response = lMisc.fail(response[2])
            else:
                data_response = (int(response[4]) << 8) + int(response[3])
        else:
            data_response = lMisc.fail(55)
            
        logging.debug(data_response)
        return data_response
    
    
    def analogreadbattery(self):  # Get the current battery status as an analog value
        """
        Getter analog battery 
        
        :return: response
        :rType: Integer [volt with value/1000]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        _rNumber = self._robot.getRNumber()
        order = [_rNumber, 3, 205]
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
            if response[2] != '106':
                data_response = lMisc.fail(response[2])
            else:
                data_response = (int(response[4]) << 8) + int(response[3])
        else:
            data_response = lMisc.fail(55)
            
        logging.debug(data_response)
        return data_response
    
    
    def analogreaddistanceleft(self):  # Get the analog values of the distance sensors on the left side
        """
        Getter analog distance left 
        
        :return: distance left
        :rType: tuple [0,0,0,0]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        _rNumber = self._robot.getRNumber()
        order = [_rNumber, 4, 6, 1]
        data_response = []
        response = self._communication.send_receive(order)
        i = 0
        while response == 'fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return self.fail(20)
            i = i + 1
        while int(response[0]) != _rNumber:
            response = self._communication.receive(order)
        if int(response[0]) == _rNumber:
            if response[2] != '111':
                data_response = self.fail(response[2])
            else:
                data_response.append(((int(response[3]) << 2) & 0xffff) + ((int(response[4]) >> 6) & 0xffff))
                data_response.append(((((int(response[4]) << 10) & 0xffff) >> 6) & 0xffff) + ((int(response[5]) >> 4) & 
                                                                                              0xffff))
                data_response.append(((((int(response[5]) << 12) & 0xffff) >> 6) & 0xffff) + ((int(response[6]) >> 2) & 
                                                                                              0xffff))
                data_response.append(((((int(response[6]) << 14) & 0xffff) >> 6) & 0xffff) + int(response[7]))
        else:
            data_response = self.fail(55)
        
        logging.debug(data_response)
        return data_response
    
    
    def analogreaddistanceright(self):  # Get the analog values of the distance sensors on the right side
        """
        Getter analog distance right 
        
        :return: distance right
        :rType: tuple [0,0,0,0]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        _rNumber = self._robot.getRNumber()
        order = [_rNumber, 4, 6, 2]
        data_response = []
        response = self._communication.send_receive(order)
        i = 0
        while response == 'fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return self.fail(20)
            i = i + 1
        while int(response[0]) != _rNumber:
            response = self._communication.receive(order)
        if int(response[0]) == _rNumber:
            if response[2] != '112':
                data_response = self.fail(response[2])
            else:
                data_response.append(((int(response[3]) << 2) & 0xffff) + ((int(response[4]) >> 6) & 0xffff))
                data_response.append(((((int(response[4]) << 10) & 0xffff) >> 6) & 0xffff) + ((int(response[5]) >> 4) & 
                                                                                              0xffff))
                data_response.append(((((int(response[5]) << 12) & 0xffff) >> 6) & 0xffff) + ((int(response[6]) >> 2) & 
                                                                                              0xffff))
                data_response.append(((((int(response[6]) << 14) & 0xffff) >> 6) & 0xffff) + int(response[7]))
        else:
            data_response = self.fail(55)
        
        logging.debug(data_response)
        return data_response    
