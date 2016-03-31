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
import ldvbot


class robot:
    '''
    Main API class robot
    '''


    def __init__(self, rNumber=None):
        """
        Constructor 
        
        :parameter: rNumber (default=None) used for ldvbot
        :pType: integer
        """
        # logging.basicConfig(filename='robot.log', level=logging.DEBUG)
        # Logging with filemode='w' overrides file
        logging.basicConfig(filename='robot.log', filemode='w', level=logging.DEBUG)
     
    def getEpuck(self):
        """
        Getter ePuck 
        
        :return: ePuck
        :rType: epuck.robot
        """
        return epuck.robot()
    
    def getLdvBot(self, rNumber):
        """
        Getter LDVbot 
        
        :return: LDVbot
        :rType: ldvbot.robot
        """
        return ldvbot.robot(rNumber)   