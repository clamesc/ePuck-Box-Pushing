import graphviz as gv
import numpy as np

if __name__ == "__main__":
    T = np.load("T.npy")
    Pt = np.zeros((T.shape[0], T.shape[0]))
    for s in range(T.shape[0]):  # iterate over old states
        Pt[s] = np.zeros(T.shape[0])
        for a in range(T.shape[1]):
            Pt[s] += T[s][a]
        Pt[s] = Pt[s] / np.sum(Pt[s])
    print Pt

    dot = gv.Digraph(comment='The Round Table')
    dot.node(str(0), 'desired direction')
    for i in range(1, T.shape[0]):
        dot.node(str(i))
        for t in range(Pt.shape[1]):
            if Pt[i][t] != 0.0:
                dot.edge(str(i), str(t), label=str("%0.2f" % Pt[i][t]))

    print dot.source
    dot.render('state_transisitions', view=True)
