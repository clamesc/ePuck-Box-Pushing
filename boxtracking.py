                                                                                               #!/usr/bin/python

import math
import numpy as np
import operator
from cmath import rect, phase
from math import radians, degrees
from random import randint
from time import sleep
from robot.robot import robot
import boxtracking


def get_box_position(proximity_values=(3739, 256, 55, 75, 113, 87, 786, 3810, 3903, 3882), deg=True):
    '''
    Proximity values:

    pos     robot

    -135      3
    -90       2
    -45       1
    -10       0
    +10       7
    +45       6
    +90       5
    +135      4
    '''

    proximity_data = np.loadtxt('proximity_values.txt')
    target_values = np.arange(-18, 18) * 10
    proximity_values = np.array(proximity_values[:8])
    neighbors, distances = getNeighbors(proximity_data, proximity_values, 3)
    angles = target_values[neighbors]
    if deg:
        return weightedMean(angles, distances)
    else:
        return radians(weightedMean(angles, distances))


def getNeighbors(trainingSet, testInstance, k):
    length = len(trainingSet)
    distances = np.zeros((length, 2))
    for x in range(length):
        distances[x, :] = [x, euclideanDistance(testInstance, trainingSet[x])]
    distances = distances[distances[:, 1].argsort()]
    return distances[:k, 0].astype(int), distances[:k, 1]


def euclideanDistance(instance1, instance2):
    distance = 0
    for x in range(instance1.shape[0]):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def weightedMean(targets, distances):
    mean = 0
    weights = 0
    for i in range(distances.shape[0]):
        weights += (1 / distances[i])
        mean += (1 / distances[i]) * targets[i]
    return mean / weights


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
