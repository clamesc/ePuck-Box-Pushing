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


def fail(data):  # Checks if a correct/expected response has been received
    if data == 198:
        output = 198
    elif data == 199:
        output = 199
    elif data == 55:
        output = 55
        logging.warn('WARNING: No Response from remote device. (Check your wireless connection)')
    elif data == 20:
        output = 'fail'
        logging.warn("Warning: NRF-transmission failed")
    else:
        output = 15
        logging.error("ERROR: Exception thrown - Fail function called (received unexpected value!)")
    return output
  
def to_bin(decimal, bits):  # Converts decimal values into binary ones
    tmp_value = bin(int(decimal))[2:].zfill(bits)
    return tmp_value  
