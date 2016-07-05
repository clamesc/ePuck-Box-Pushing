import graphviz as gv
import numpy as np
import math

# Gives back 2D Array [Actions x Resulting State]
def transitions():
    T = np.load("T.npy")
    t = np.zeros((3,5))
    for a in range(T.shape[1]):
        for s in range(T.shape[0]):
            ll_ind = (s-2)%10
            l_ind = (s-1)%10
            rr_ind = (s+2)%10
            r_ind = (s+1)%10
            t[a,0] += T[s,a,ll_ind]
            t[a,1] += T[s,a,l_ind]
            t[a,2] += T[s,a,s]
            t[a,3] += T[s,a,r_ind]
            t[a,4] += T[s,a,rr_ind]
    for a in range(t.shape[0]):
        t[a] = t[a]/sum(t[a])
    return t

def calc_circlepos(i, i_max):
    radius = 3
    posx = math.cos((math.pi * 2.0 * float(i) / float(i_max)) - 1.5 * math.pi) * radius
    posy = math.sin((math.pi * 2.0 * float(i) / float(i_max)) - 1.5 * math.pi) * radius
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
            if Pt[i][t] != 0.0:
                dot.edge(str(i), str(t), label=str("%0.2f" % Pt[i][t]))

    print dot.source
    dot.render('state_transisitions', view=True)
