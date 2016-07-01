#!/usr/bin/python
from random import randint
from time import sleep
import math
import numpy as np
from robot.robot import robot
import boxtracking


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
    return boxtracking.get_box_position(resp)


def get_reward(current_state):
    if current_state == int(desiredDirection // delta):
        return 100
    else:
        return 0

if __name__ == '__main__':
    try:
        epuck = robot().getEpuck()
        epuck.connect()
        raw_input("Press Enter to continue...")

        # Qlearning parameters
        alpha = 0.5
        gamma = 0.8
        desiredDirection = 0
        nbOfActions = 3  # has to be an odd number
        nbOfStates = 10
        turnAngle = 45
        stepsize = 90
        episode = int(np.loadtxt("e.txt"))#1
        orientation = 0
        greedyFactor = 0.4
        delta = 360.0 / nbOfStates
        Q = np.loadtxt("Q.txt") #np.zeros((nbOfStates, nbOfActions))

        while True:
            robOri = initialise_state()
            print "Orientation: " + str(robOri)

            current_state = get_current_state(robOri)
            print "State: " + str(current_state)

            while True:
                if current_state == 0:
                    action = choose_action(current_state, episode)
                    print "Action: " + str(action)

                    robOri = do_action(robOri, action)
                    print "Orientation:" + str(robOri)

                    new_state = get_current_state(robOri)
                    print "New state:" + str(new_state)

                    R = get_reward(new_state)
                    Q[current_state, action] = Q[current_state, action] + alpha * \
                        (R + gamma * max(Q[new_state, :]) - Q[current_state, action])

                    episode += 1

                    print "Q values:"
                    print Q
                    print ""

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

                current_state = new_state
    finally:
        np.savetxt('Q.txt',Q)
        np.savetxt('e.txt',[episode])
        epuck = robot().getEpuck()
        epuck.connect()
        epuck.reset()
        epuck.disconnect()
