#!/usr/bin/python

import numpy as np
from robot.robot import robot

class boxtracking:
    epuck = None
    position = []

    def __init__(self):
        self.epuck = robot().getEpuck()
        self.epuck.connect()

    def prox(self):
        resp = self.epuck.getProximitySensor().getValues()
        while type(resp) == bool:
            resp = self.epuck.getProximitySensor().getValues()
        return resp
    
    def record(self):
        values = []
        for i in range(20):
            values.append(self.prox()[:8])
        position.append(np.mean(values, axis=0))

    def save(self):
        np.savetxt('proximity_values.txt', np.array(self.position))
