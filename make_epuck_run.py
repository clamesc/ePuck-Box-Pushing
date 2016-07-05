#!/usr/bin/python
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
    """ Calculates the euclidean distance between two vectors.
        We have to re-implement this because the version of numpy is too low
        on the ePuck
    """
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


def do_round(orientation):
    global alpha, gamma
    current_state = get_current_state(orientation)
    print "Old State: " + str(current_state)
    action = choose_action(current_state, episode)
    print "Action   : " + str(action)

    orientation = do_action(orientation, action)

    new_state = get_current_state(orientation)
    print "New state: " + str(new_state)

    R = get_reward(new_state)
    Q[current_state, action] = Q[current_state, action] + alpha * \
        (R + gamma * max(Q[new_state, :]) - Q[current_state, action])

    T[current_state, action, new_state] += 1

    print "Q values:"
    print Q
    print ""
    return orientation


def end_episode(orientation, episode):
    orientation = do_round(orientation)
    try:
        Q_old = np.load("Q.npy")
        s_old = np.load("s.npy")
        np.save("Q.npy", np.concatenate(
            (Q_old, np.reshape(Q, (1, Q.shape[0], Q.shape[1]))), axis=0))
        np.save("s.npy", np.concatenate((s_old, [episodeSteps]), axis=0))
    except:
        np.save("Q.npy", np.reshape(Q, (1, Q.shape[0], Q.shape[1])))
        np.save("s.npy", np.reshape([episodeSteps], (1)))
    finally:
        np.save("T.npy", T)

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
        global alpha, gamma, desiredDirection, nbOfActions, nbOfStates, \
            turnAngle, stepsize, episode, greedyFactor, delta, Q, T

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
            episode = np.load("s.npy").shape[0]
        except:
            episode = 1
        try:
            Q = np.load("Q.npy")[-1]
        except:
            Q = np.zeros((nbOfStates, nbOfActions))
        try:
            T = np.load("T.npy")
        except:
            T = np.zeros((nbOfStates, nbOfActions, nbOfStates))

        while True:  # This iterates over complete episodes
            episodeSteps = 0
            robOri = initialise_state()
            while True:  # This iterates over rounds in an episode
                if get_current_state(robOri) == desiredDirection:
                    break
                robOri = do_round(robOri)
                episodeSteps += 1
            end_episode(robOri, episode)
            episode += 1
    finally:
        epuck = robot().getEpuck()
        epuck.connect()
        epuck.reset()
        epuck.disconnect()
