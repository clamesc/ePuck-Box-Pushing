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

import serial

import epuck
import eCamera


'lines of ePuck responses'
DIC_MSG = {
    "v": 2,  # Version
    "\n": 23,  # Menu
    "\x0c": 2,  # Welcome
    "k": 2,  # Calibration
    "R": 2  # Reset
}

class communication:
    '''
    Communication ePuck
    '''


    def __init__(self, bot):
        """
        Constructor 
        
        :parameter: bot
        :pType: epuck.robot
        """
        
        if isinstance(bot, epuck.robot):
            self._robot = bot
        else:
            logging.error('Parameter has to be of type robot')
            raise ValueError("Parameter has to be of type robot")
    

    def send_binary_mode_epuck(self, parameters):
        """
        Send binary mode ePuck used to receive sensor values
        
        :parameter    parameter: Receive request ('Char to be sent', 'Size of reply waited', 'Format of the reply')
        :pTtype    message: tuple
        :return: response
        :rType: tuple
        """
        message = struct.pack(">bb", -ord(parameters[0]), 0)
        self.send(message)
        response = self.receive()
        
        i = 0
        while len(response) < parameters[1]:
            response += self.receive()
            
            i = i+1
            
            if i == 150 and len(response) == 0:
                logging.debug('No messages received for 150 steps')
                return False
                break
        if len(response) != parameters[1]:
            logging.debug('Wrong length of response message. Length is ' + str(len(response)) + 'and requested length was' + str(parameters[1]))
            return False
        
        response = struct.unpack(parameters[2], response)

        return response
        
    def write_actuators_epuck(self, order):
        """
        Write parameter to ePuck
        
        :parameter order
        :pType tuple
        """
        
        acks = ['j', 't', 'ds']

        if order[0] == 'L':
            # Leds
            message = struct.pack('<bbbb', -ord(order[0]), order[1], order[2], 0)
            n = self.send(message)
            unpacked_msg = struct.unpack('<bbbb', message)
            cmd = chr(-unpacked_msg[0])
            logging.debug('Binary message of ' + str(n) + ' bytes sent: ' + str(unpacked_msg) + '; ' + str(unpacked_msg[0]) + '=' + cmd)

        elif order[0] == 'D' or order[0] == 'P':
            # Set motor speed or set motor position
            message = struct.pack('<bhhb', -ord(order[0]), order[1], order[2], 0)
            n = self.send(message)
            unpacked_msg = struct.unpack('<bhhb', message)
            cmd = chr(-unpacked_msg[0])
            logging.debug('Binary message of ' + str(n) + ' bytes sent: ' + str(unpacked_msg) + '; ' + str(unpacked_msg[0]) + '=' + cmd)

        else:
            # Others actuators, parameters are separated by commas
            message = ",".join(["%s" % i for i in order])
            logging.debug(message)
            response = self.send_receive(message)
            if response == 'j':
                eCamera.camera(self._robot).refresh_camera_parameters()

            if response not in acks:
                logging.debug('Unknown ACK reply from ePuck: ' + response)
            
            
    def send(self, msg):
        """
        send to ePuck
        
        :parameter message
        :type string
        :return: Number of bytes sent if it was successful. -1 if not
        :rType: integer
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'

        try:
            response = self._robot.getPort().write(msg)
            # Simple hack for backwards compatibility (n is only returned since pySerial 2.5)
            if response == None:
                response = len(msg)
                
        except Exception, e:
            logging.debug('ePuck send exception: ' + e)
            return False
        else:
            return response
        
    def receive(self, n=128):
        """
        receive from ePuck
        
        :parameter n (bytes to receive)
        :pType integer
        :return: Data received from the robot as string if it was successful, raise an exception if not
        :rType: string
        :raise Exception:    If there is a communication problem
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'

        try:
            line = self._robot.getPort().read(n)
        except serial.SerialException as e:
            logging.exception('Serial communication problem: ' + str(e))
            raise Exception, 'Serial communication problem: ' + str(e)
        else:
            return line
        
    def send_receive(self, msg):
        """
        Send_receive method ePuck
        
        :param msg: The message you want to send
        :type msg: String
        :return: Response of the robot
        :rtype: String
        """

        # Check the connection
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'

        # Make sure the Message is a string
        message = str(msg)

        # Add carriage return if not
        if not message.endswith('\n'):
            message += '\n'

        # Check the lines of the waited reply
        if message[0] in DIC_MSG:
            lines = DIC_MSG[message[0]]
        else:
            lines = 1
        logging.debug('Waited lines: '+ str(lines))

        # We make 5 tries before desist
        tries = 1
        while tries < 5:
            # Send the message
            self.send(message)
            try:
                # Receive the reply. As we want to receive a line, we have to insist
                reply = ''
                while reply.count('\n') < lines:
                    reply += self.receive()
                    if message[0] == 'R':
                        # For some reason that I don't understand, if you send a reset
                        # command 'R', sometimes you recive 1 or 2 lines of 'z,Command not found\r\n'
                        # Therefore I have to remove it from the expected message: The Hello message
                        reply = reply.replace('z,Command not found\r\n', '')
                return reply.replace('\r\n', '')

            except Exception:
                tries += 1         
                logging.debug('Communication timeout, retrying')
