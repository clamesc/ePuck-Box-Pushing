import graphviz as gv
import numpy as np
import math


def transitions(T):
    """ Gives back 2D Array [Actions x Resulting State]
    """
    t = np.zeros((3, 5))
    for a in range(T.shape[1]):
        for s in range(T.shape[0]):
            ll_ind = (s - 2) % 10
            l_ind = (s - 1) % 10
            rr_ind = (s + 2) % 10
            r_ind = (s + 1) % 10
            t[a, 0] += T[s, a, ll_ind]
            t[a, 1] += T[s, a, l_ind]
            t[a, 2] += T[s, a, s]
            t[a, 3] += T[s, a, r_ind]
            t[a, 4] += T[s, a, rr_ind]
    for a in range(t.shape[0]):
        t[a] = t[a] / sum(t[a])
    return t


def calc_circlepos(i, i_max, radius=2):
    posx = math.cos((math.pi * 2.0 * float(i) / float(i_max)) - 1.5 * math.pi) * radius
    posy = math.sin((math.pi * 2.0 * float(i) / float(i_max)) - 1.5 * math.pi) * radius
    return "{},{}!".format(posx, posy)


def calc_ori(i, i_max):
    return str(math.degrees(math.pi * 2.0 * float(i) / float(i_max)) - 1.5 * math.pi)


def calc_linepos(i, i_max):
    posy = 0
    posx = i + i_max / 2
    return "{},{}!".format(posx, posy)

if __name__ == "__main__":
    T = np.load("Data/2016_07_05-2_T.npy")
    Pt = np.zeros((T.shape[0], T.shape[0]))
    for s in range(T.shape[0]):  # iterate over old states
        Pt[s] = np.zeros(T.shape[0])
        for a in range(T.shape[1]):  # iterate over actions
            Pt[s] += T[s][a]
        Pt[s] = Pt[s] / np.sum(Pt[s])
    print Pt

    dot = gv.Digraph(comment='State Transition Probabilities',
                     graph_attr={('layout', 'neato')},
                     node_attr={('shape', 'circle')}
                     )
    for i in range(0, T.shape[0]):
        if i == 0:
            dot.node(str(i), shape='doublecircle', pos=calc_circlepos(i, T.shape[0]))
        else:
            dot.node(str(i), pos=calc_circlepos(i, T.shape[0]))
        for t in range(Pt.shape[1]):
            if Pt[i][t] > 0.004:
                dot.edge(str(i), str(t), label=str("%0.2f" % Pt[i][t]),
                         location=calc_circlepos(i, T.shape[0], 2.4))

    print dot.source
    dot.render('state_transisitions', view=False)

    tr = transitions(T)
    dot2 = gv.Digraph(comment='Average State Transition Probabilities',
                      node_attr={('shape', 'circle')},
                      graph_attr={('layout', 'neato')})

    for a in range(tr.shape[0]):
        for s in range(tr.shape[1]):
            if a == 0:
                dot2.node(str(s), pos=calc_linepos(s, tr.shape[1]))

    for a in range(tr.shape[0]):
        for s in range(tr.shape[1]):
            print str(a) + " " + str(s)
            if tr[a][s] > 0.0004:
                dot2.edge(str(a), str(s), label=str("%0.3f" % tr[a][s]))
    print dot2.source
    dot2.render('average_state_transisitions', view=True)
