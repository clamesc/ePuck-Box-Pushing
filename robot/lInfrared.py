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
import time

import ldvbot
import lCommunication
import lMisc

class infrared():
    '''
    infrared LDVbot
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
        
    def getID(self, robotNr):  # Get the current infrared ID from robot
        """
        Getter infrared id 
        
        :parameter: robotNr
        :pType: Integer
        :return: infrared id
        :rType: Integer [0,7]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        order = [robotNr, 3, 9]
        response = self._communication.send_receive(order)
        i = 0
        while response == 'misc.fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while (int(response[0]) != robotNr):
            response = self._communication.receive()
        if int(response[0]) == robotNr:
            if response[2] != '47':
                data_response = lMisc.fail(response[2])
            else:
                data_response = response[3]
        else:
            data_response = lMisc.fail(55)
        
        logging.debug(data_response)
        return data_response
    
    def setID(self, robotNr, infra_id):  # Set infrared ID of the robot
        """
        Setter infrared id 
        
        :parameter: robotNr
        :pType: Integer
        :parameter: infra_id
        :pType: Integer [0,7]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if (infra_id < 0) or (infra_id > 7):
            raise ValueError('ERROR: Invalid parameter for "receiver_id"! (0-7 expected)')
        order = [robotNr, 4, 10, infra_id]
        logging.debug(order)
        response = self._communication.send(order)           
        i = 0                                           
        while response == 'misc.fail':                       
            response = self._communication.send(order)      
            if i > 4:                                   
                return lMisc.fail(20)
            i = i + 1                                     
    
    def getSensitivity(self, robotNr):  # Get the current infrared sensitivity from robot
        """
        Getter infrared sensitivity 
        
        :parameter: robotNr
        :pType: Integer
        :return: infrared sensitivity
        :rType: Integer [0,1023]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        order = [robotNr, 3, 12]
        response = self._communication.send_receive(order)
        i = 0
        while response == 'misc.fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while (int(response[0]) != robotNr):
            response = self._communication.receive()
        if int(response[0]) == robotNr:
            if response[2] != '50':
                data_response = lMisc.fail(response[2])
            else:
                data_response = (int(response[4]) << 8) + int(response[3])
        else:
            data_response = lMisc.fail(55)
            
        logging.debug(data_response)
        return data_response
    
    def setSensitivity(self, robotNr, sens):  # Set the threshold value for the distance sensors
        """
        Setter infrared sensitivity 
        
        :parameter: robotNr
        :pType: Integer
        :parameter: sens
        :pType: Integer [0,1023]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'

        if not 0 <= sens < 1023:
            raise ValueError('ERROR: Invalid parameter for "sens"! (0 - 1023 expected)')
        sens_tmp = struct.unpack('BB', struct.pack('H', sens))
        sens_int1 = sens_tmp[0]
        sens_int2 = sens_tmp[1]
        order = [robotNr, 5, 13, sens_int1, sens_int2]
        logging.debug(order)
        response = self._communication.send(order)           
        i = 0                                           
        while response == 'misc.fail':                       
            response = self._communication.send(order)       
            if i > 4:                                   
                return lMisc.fail(20)
            i = i + 1                                     
    
    
    def setReceiveMode(self, robotNr):  # Set robot into receive mode
        """
        Setter receive mode 
        
        :parameter: robotNr
        :pType: Integer
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        order = [robotNr, 3, 8]
        logging.debug(order)
        self._communication.send(order)
        # response = self._communication.send(order)           
        # i=0
        # while response=='misc.fail':
        #    response = self._communication.send(order)
        #    if i>4:
        #        return misc.fail(20)
        #    i=i+1
    
    def send(self, sender_rbn, receiver_id, data_byte):  # Send IR package
        """
        send infrared 
        
        :parameter: sender_rbn
        :pType: Integer
        :paramter: receiver_id
        :pType: Integer [0,7]
        :paramter: data_byte
        :pType: Integer [0,255]
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if (receiver_id < 0) or (receiver_id > 7):
            raise ValueError('ERROR: Invalid parameter for "receiver_id"! (0-7 expected)')
        if (data_byte < 0) or (data_byte > 255):
            raise ValueError('ERROR: Invalid parameter for "data_byte"! (0-255 expected)')
        order = [sender_rbn, 5, 7, receiver_id, data_byte]
        data_response = []
        response = self._communication.send_receive(order)
        i = 0
        while response == 'misc.fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while int(response[0]) != sender_rbn:
            response = self._communication.receive(order)
        if int(response[0]) == sender_rbn:
            if response[2] != '45':
                data_response = lMisc.fail(response[2])
            else:
                data_response.append(int(response[3]))
                data_response.append(int(response[4]))
        else:
            data_response = lMisc.fail(55)
            
        logging.debug(data_response)
        return data_response
    
    
    
    def getLastValues(self, robotNr):  # Get last IR values of robot
        """
        Getter infrared values 
        
        :parameter: robotNr
        :pType: Integer
        :return: infrared values
        :rType: tuple
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        order = [robotNr, 3, 11]
        data_response = []
        response = self._communication.send_receive(order)
        i = 0
        while response == 'misc.fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while int(response[0]) != robotNr:
            response = self._communication.receive()
        if int(response[0]) == robotNr:
            if response[2] != '49':
                data_response = lMisc.fail(response[2])
            else:
                data_response.append(int(response[3]))
                data_response.append(int(response[4]))
                data_response.append(int(response[5]))
        else:
            data_response = lMisc.fail(55)
            
        logging.debug(data_response)
        return data_response
    
    
    def getSensorWord(self, robotNr, sensor):  # Debug
        """
        Getter sensor word
        
        :parameter: sensor
        :pType: Integer
        :return: sensor word
        :rType: tuple
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        if (sensor - 1 < 0) or (sensor - 1 > 7):
            raise ValueError('ERROR: Invalid parameter for "sensor"! (1-8 expected)')
    
        order = [robotNr, 4, 14, sensor]
        data_response = []
        response = self._communication.send_receive(order)
        i = 0
        while response == 'misc.fail':
            response = self._communication.send_receive(order)
            if i > 4:
                return lMisc.fail(20)
            i = i + 1
        while int(response[0]) != robotNr:
            response = self._communication.receive()
        if int(response[0]) == robotNr:
            if response[2] != '60':
                data_response = lMisc.fail(response[2])
            else:
                data_response.append(int(response[3]))
                data_response.append(int(response[4]))
        else:
            data_response = lMisc.fail(55)
            
        logging.debug(data_response)
        return data_response
    
    
    ##### Exemplarische Benutzung der IR-Funktionen
    def init(self, sender_rbn, receiver_rbn, sender_id, receiver_id, sensitivity):
        """
        Init infrared
        example
        
        :parameter: sender_rbn, reveiver_rbn, sender_id, receiver_id, sensitivity
        """
    
        self.setID(sender_rbn, sender_id)
        self.setID(receiver_rbn, receiver_id)
        self.setSensitivity(sender_rbn, sensitivity)
        self.setSensitivity(receiver_rbn, sensitivity)
        logging.info('Initialized')
    
    
    def sendWord(self, sender_rbn, receiver_rbn, receiver_id, byte):
        """
        Send infrared word 
        
        :parameter: sender_rbn, reveiver_rbn, receiver_id, byte
        """
        time.sleep(0.1)
        self.setReceiveMode(receiver_rbn)
        time.sleep(0.1)
        self.send(sender_rbn, receiver_id, byte)
        time.sleep(1)
        last_data = self.getLastValues(receiver_rbn)
        received_id = int(last_data[0]) >> 5
        received_byte = int(last_data[1])
        received_direction = int(last_data[0]) & 0x1F
        received_distance = int(last_data[2])
        logging.info("Received ID:")
        logging.info(received_id)
        logging.info("Received Byte:")
        logging.info(received_byte)
        logging.info("Received direction:")
        logging.info(received_direction)
        logging.info("Received distance:")
        logging.info(received_distance)
