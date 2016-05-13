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

class communication:
    '''
    communication LDVbot
    '''


    def __init__(self, bot):
        """
        Constructor 
        
        :parameter: bot
        :pType: ldvbot.robot
        """
        
        if isinstance(bot, ldvbot.robot):
            self._robot = bot
        else:
            logging.error('Parameter has to be of type robot')
            raise ValueError("Parameter has to be of type robot")
                 
                          
    def send(self, msg): 
        """
        Send method LDVbot
        
        :param   msg: message parameter
        :type    msg: tuple
        :return: response
        :rtype:  String
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        while not self._robot.getPort().readable():
            pass
        self._robot.getPort().write(msg)
        
        inQueue = 0
        while self._robot.getPort().inWaiting() == 0:
            if inQueue > 200000:
                return 'fail'
            inQueue = inQueue + 1
        
        data = (self._robot.getPort().readline()).rstrip('\r\n')
        
        if data != 'transmitted ':
            return 'fail'
        else:
            return 0 

    def receive(self):  
        """
        Receive method LDVbot
        
        :return: response
        :rtype:  String
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        while not self._robot.getPort().readable():
            pass
        lines = []
    
        run = 0
        while run < 8:
            inQueue = 0
            while self._robot.getPort().inWaiting() == 0:
                if inQueue > 100000:
                    return 'fail'
                inQueue = inQueue + 1
                
            data = self._robot.getPort().readline()
            lines.append(data.rstrip('\r\n'))
            run = run + 1
        if 1 < len(lines):
            logging.info("Received Response:", lines[2])
            return lines
    
    
    def send_receive(self, msg):  # Sends a command to the robot and receives its response
        """
        Send_receive LDVbot
        
        :param   msg: Request
        :type    message: tuple
        :return: response
        :rtype:  String
        """
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        while not self._robot.getPort().readable():
            pass
        while not self._robot.getPort().inWaiting() == 0:
            self._robot.getPort().readline()
        while not self._robot.getPort().readable():
            pass
        self._robot.getPort().write(msg)
        lines = []
    
        run = 0
        while run < 9:
            inQueue = 0
            while self._robot.getPort().inWaiting() == 0:
                if inQueue > 200000:
                    return 'fail'
                inQueue = inQueue + 1
                
            data = self._robot.getPort().readline()
            lines.append(data.rstrip('\r\n'))
            run = run + 1
            
        if lines[0] != 'transmitted ':
            return 'fail'
        else:
            reponseLine = 1
            while reponseLine < 9:
                lines[reponseLine - 1] = lines[reponseLine]
                reponseLine = reponseLine + 1
        
        if 1 < len(lines):
            return lines      
