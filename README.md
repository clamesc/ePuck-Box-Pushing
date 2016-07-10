# ePuck Box-Pushing Project

This is the final code for the Applied RL class in SS2016 for the only ePuck group consisting of

Claus Meschede
Jan Rudolph
José Luís Gaytán

It contains a unmodified copy of the code from the LDV RobotAPI repository in the [robot folder](robot).

## Collected Data

The [Data folder](Data) contains training data collected during test runs.
2016_07_05-2 is the set of data used for the graphs in the final report.

- The Q.npy contains the history of Q values after every episode.
- The s.npy contains the number of steps needed for every episode.
- The T.npy contains the average state/action transition probabilities.

You can use the [plot](plot.py) script to reproduce the QValues/learning curve graph from the final report.
The average state/action transition graph is created manually using the matrix in T.

## Main Scripts

In order to retrieve distance sensor calibration parameters for the boxtracking algorithm, you can use
the boxtracking class from the [boxtracking_calibration file](boxtracking_calibration.py).
The proximity_values.txt in this zipfile was taken for the ePuck with the ip address 192.168.1.203.

The [make_epuck_run](make_epuck_run.py) script is the one we used for training.

The [show](show.py) script is the same script, the only difference is that it uses 100% greedy actions.

