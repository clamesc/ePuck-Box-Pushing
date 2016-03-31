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
import time  # Used for image capture process

import eCommunication
import epuck
from PIL import Image


# mode of the camera
CAM_MODE = {
    "GREY_SCALE"    : 0,
    "RGB_365"        : 1,
    "YUV"            : 2,
    "LINEAR_CAM"    : 3
    }

# camera zoom
CAM_ZOOM = (1, 4, 8)

class camera:
    '''
    Camera ePuck
    Doesn't work. Reused code of the old API failed. 
    ePuck doesn't respond to message 'I' used to refresh camera parameters
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
            
            # Camera attributes
            self._cam_width = None
            self._cam_height = None
            self._cam_enable = False
            self._cam_zoom = None
            self._cam_mode = None
            self._cam_size = None
            self._pil_image = None
            
            self._camera_parameters = (0, 0, 0, 0)
                
        else:
            logging.error('Parameter has to be of type robot')
            raise ValueError("Parameter has to be of type robot") 

    def set_camera_parameters(self, mode, width, height, zoom):
        """
        Setter camera parameter
        
        :parameter mode: GREY_SCALE, LINEAR_CAM, RGB_365, YUM
        :pType  mode: string
        :parameter width: Width of the camera
        :pType  width: integer
        :parameter height: Height of the camera
        :pType  height: integer
        :parameter zoom: 1, 4, 8
        :pType  zoom: integer
        """

        if mode in CAM_MODE:
            self._cam_mode = CAM_MODE[mode]
        else:
            return -1

        if int(zoom) in CAM_ZOOM:
            self._cam_zoom = zoom
        else:
            return -1

        if self._robot.getConnectionStatus() and int(width) * int(height) <= 1600:
            # 1600 are for the resolution no greater than 40x40, I have
            # detect some problems
            self._communication.write_actuators_epuck("J", self._cam_mode, width, height, self._cam_zoom)
            return 0
               
    def refresh_camera_parameters(self):
        """
        refresh camera parameter
        """
        try:
            logging.debug('before response')
            response = self._communication.send_receive("I").split(',')
            logging.debug(response)
        except:
            logging.debug(False)
            return False
        else:
            self._cam_mode, \
            self._cam_width, \
            self._cam_height, \
            self._cam_zoom, \
            self._cam_size = [int(i) for i in response[1:6]]

            self._camera_parameters = self._cam_mode, self._cam_width, self._cam_height, self._cam_zoom
            logging.debug(self._camera_parameters)
            
    def save_image(self, name='ePuck.jpg'):
        """
        Save image from camera to disk
        
        :parameter name: Image name, ePuck.jpg as default
        :pType name: String
        
        :return: operation result
        :rType: Boolean
        """

        if self._pil_image:
            return self._pil_image.save(name)
        else:
            return False
        
    def get_image(self):
        """
        return image from ePuck
        Recommended: not more then 1 image per second
        
        :return: The image in PIL format
        :rType: PIL Image
        """
        
        if not self._robot.getConnectionStatus():
            logging.exception('No connection available')
            raise Exception, 'No connection available'
        
        # Thanks to http://www.dailyenigma.org/e-puck-cam.shtml for
        # the code for get the image from the camera
        msg = struct.pack(">bb", -ord("I"), 0)
        
        try:
            logging.debug('before refresh')
            self._refresh_camera_parameters()
            self._cam_enable = True
            self.timestamp = time.time()

            logging.debug('after refresh')
            n = self._communication.send(msg)
            logging.debug("Reading Image: sending " + repr(msg) + " and " + str(n) + " bytes")

            # We have to add 3 to the size, because with the image we
            # get "mode", "width" and "height"
            size = self._cam_size + 3
            img = self._communication.receive(size)
            while len(img) != size:
                img += self._communication.receive(size)

            # Create the PIL Image       
            image = Image.frombuffer("RGB", (self._cam_width, self._cam_height), img, "raw", "BGR;16", 0, 1)
            image = image.rotate(180)
            self._pil_image = image

        except Exception, e:
            logging.debug('Problem receiving an image: ' + str(e))
        

