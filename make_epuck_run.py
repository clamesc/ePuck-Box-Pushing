#!/usr/bin/python
from random import randint
from time import sleep
import math
import numpy as np
from robot.robot import robot
from math import radians


def initialise_state():
    return np.random.randint(360)

def choose_action(current_state, episode):
    eps = 1.0 / np.power(episode, greedyFactor)
    # Select max Q values
    qmax = np.argwhere(Q[current_state, :] == np.amax(Q[current_state, :]))[:, 0]
    # Select random Q from max Q values as greedy action
    qmax = qmax[np.random.randint(qmax.shape[0])]
    # Define probabilities for non-greedy actions
    p_nonGreedy = eps / nbOfActions
    # Deine probability for greedy action
    p_greedy = 1 - p_nonGreedy * (nbOfActions - 1)
    # Randomly choose action from distribution
    greedy = np.random.binomial(1, p_greedy) == 1
    if greedy:
        return np.arange(nbOfActions)[qmax]
    else:
        i = np.random.randint(nbOfActions - 1)
        return np.delete(np.arange(nbOfActions), qmax)[i]

def do_action(orientation, action):
    action = action - (nbOfActions // 2)
    # As the box tracking is most precise in the front, we first turn
    # the ePuck so that the box is in front of it
    old_boxpos = box_position()
    epuck.getMotor().drive(speed=0, dist=0, angle=old_boxpos)
    sleep(1)

    # Now we get a new estimate of the box position
    boxpos = box_position()

    print "Boxposition: " + str(boxpos)
    print 'Turn: ' + str(boxpos + action * turnAngle)

    new_orientation = old_boxpos + boxpos + action * turnAngle

    epuck.getMotor().drive(speed=0, dist=0, angle=(boxpos + action * turnAngle))
    sleep(1)
    epuck.getMotor().drive(speed=0, dist=stepsize, angle=0)
    sleep(1)

    # After a while, the robot does weird movements
    # This tries prevents it:
    epuck.reset()

    return (orientation + new_orientation) % (360)

def get_current_state(robOri):
    return int(get_orientation(robOri) // delta)

def get_orientation(robOri):
    return (robOri + box_position()) % (360)

def box_position():

    resp = epuck.getProximitySensor().getValues()
    # sometimes the readout fails, the while loop makes sure
    # we retry until we have a new value
    while type(resp) == bool:
        resp = epuck.getProximitySensor().getValues()
    return get_box_position(resp)

def get_reward(current_state):
    if current_state == int(desiredDirection // delta):
        return 100
    else:
        return 0

def get_box_position(proximity_values, deg=True):
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

if __name__ == '__main__':
    try:
        global epuck
        epuck = robot().getEpuck()
        epuck.connect()
        raw_input("Press Enter to continue...")
        global proximity_data, target_values
        proximity_data = np.loadtxt('proximity_values.txt')
        target_values = np.arange(-18, 18) * 10

        # Qlearning parameters global
        global alpha, gamma, desiredDirection, nbOfActions, nbOfStates, turnAngle, stepsize, episode, greedyFactor, delta, Q
        
        alpha = 0.5
        gamma = 0.8
        desiredDirection = 0
        nbOfActions = 3  # has to be an odd number
        nbOfStates = 10
        turnAngle = 45
        stepsize = 90
        episodeSteps = 0
        greedyFactor = 0.4
        delta = 360.0 / nbOfStates
        
        try:
            episode = np.loadtxt("s.txt").shape[0]
        except:
            episode = 1
        try:
            Q = np.loadtxt("Q.txt")[-1]
        except:
            Q = np.zeros((nbOfStates, nbOfActions))
        
        while True:
            robOri = initialise_state()
            print "Orientation: " + str(robOri)

            current_state = get_current_state(robOri)
            print "State: " + str(current_state)

            while True:
                if current_state == desiredDirection:
                    action = choose_action(current_state, episode)
                    print "Action: " + str(action)

                    robOri = do_action(robOri, action)
                    print "Orientation:" + str(robOri)

                    new_state = get_current_state(robOri)
                    print "New state:" + str(new_state)

                    R = get_reward(new_state)
                    Q[current_state, action] = Q[current_state, action] + alpha * \
                        (R + gamma * max(Q[new_state, :]) - Q[current_state, action])

                    print "Q values:"
                    print Q
                    print ""
                    
                    try:
                        Q = np.loadtxt("Q.txt")
                        s_all = np.loadtxt("s.txt")
                        np.savetxt("Q.txt", np.concatenate((Q,Q),axis=0))
                        np.savetxt("s.txt", np.concatenate((s_all,episodeSteps),axis=0))
                    except:
                        np.savetxt("Q.txt", np.array([Q]))
                        np.savetxt("s.txt",[episodeSteps])
                    
                    episode += 1
                    break

                action = choose_action(current_state, episode)
                print "Action: " + str(action)

                robOri = do_action(robOri, action)
                print "Orientation:" + str(robOri)

                new_state = get_current_state(robOri)
                print "New state:" + str(new_state)

                R = get_reward(new_state)
                Q[current_state, action] = Q[current_state, action] + alpha * \
                    (R + gamma * max(Q[new_state, :]) - Q[current_state, action])

                print "Q values:"
                print Q
                print ""
                
                episodeSteps += 1

                current_state = new_state
    finally:
        epuck = robot().getEpuck()
        epuck.connect()
        epuck.reset()
        epuck.disconnect()
