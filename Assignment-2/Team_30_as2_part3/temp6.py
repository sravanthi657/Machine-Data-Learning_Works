import os
import json
import numpy as np
import cvxpy as cp
import logging
st = "state"
pb = "probability"
rs = "result"

accepted_positions = ["W", "N", "E", "S", "C"]
accepted_materials = [i for i in range(0, 3)]
accepted_arrows = [i for i in range(0, 4)]
accepted_states = ["D", "R"]
accepted_health = [0, 25, 50, 75, 100]

def ita(num):
    if(num==0): return "UP"
    if(num==1): return "LEFT"
    if(num==2): return "DOWN"
    if(num==3): return "RIGHT"
    if(num==4): return "STAY"
    if(num==5): return "SHOOT"
    if(num==6): return "HIT"
    if(num==7): return "CRAFT"
    if(num==8): return "GATHER"
    if(num==9): return "NONE"

accepted_actions = [ita(0), ita(1), ita(2), ita(3), ita(4), ita(5), ita(6), ita(7), ita(8), ita(9)]

def get_actions(pos, mat, arrow, state, health):
    actions = {}
    if health == 0:
        actions[ita(9)] = [
            {
                st: (pos, mat, arrow, state, health), pb: 1.0, "reward": 0.0
            }
        ]
        return actions
    if pos == "C":
        if state == "D":
            actions[ita(6)] = [
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.18, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.72, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, "R", max(0, health-50)), pb: 0.02, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, max(0, health-50)), pb: 0.08, "reward": -10.0
                }
            ]
            if arrow > 0:
                actions[ita(5)] = [
                    {
                        st: (pos, mat, arrow-1, "R", health), pb: 0.1, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, health), pb: 0.4, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, "R", max(0, health-25)), pb: 0.1, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, max(0, health-25)), pb: 0.4, "reward": -10.0
                    }
                ]
            actions[ita(1)] = [
                {
                    st: ("W", mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: ("W", mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
            actions[ita(3)] = [
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.2, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.8, "reward": -10.0
                }
            ]
            actions[ita(0)] = [
                {
                    st: ("N", mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: ("N", mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
            actions[ita(2)] = [
                {
                    st: ("S", mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: ("S", mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
        else:
            actions[ita(6)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: (pos, mat, arrow, state, max(0, health-50)), pb: 0.05, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.45, "reward": -10.0
                }
            ]
            if arrow > 0:
                actions[ita(5)] = [
                    {
                        st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, max(0, health-25)), pb: 0.25, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, health), pb: 0.25, "reward": -10.0
                    }
                ]
            actions[ita(1)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: ("W", mat, arrow, state, health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
            actions[ita(3)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.5, "reward": -10.0
                }
            ]
            actions[ita(0)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: ("N", mat, arrow, state, health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
            actions[ita(2)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: ("S", mat, arrow, state, health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
    if pos == "W":
        if state == "D":
            if arrow > 0:
                actions[ita(5)] = [
                    {
                        st: (pos, mat, arrow-1, "R", health), pb: 0.15, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, health), pb: 0.6, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, "R", max(0, health-25)), pb: 0.05, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, max(0, health-25)), pb: 0.2, "reward": -10.0
                    }
                ]
            actions[ita(3)] = [
                {
                    st: ("C", mat, arrow, "R", health), pb: 0.2, "reward": -10.0
                },
                {
                    st: ("C", mat, arrow, state, health), pb: 0.8, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.2, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.8, "reward": -10.0
                }
            ]
        else:
            if arrow > 0:
                actions[ita(5)] = [
                    {
                        st: (pos, mat, arrow-1, "D", health), pb: 0.375, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, health), pb: 0.375, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, "D", max(0, health-25)), pb: 0.125, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, max(0, health-25)), pb: 0.125, "reward": -10.0
                    }
                ]
            actions[ita(3)] = [
                {
                    st: ("C", mat, arrow, "D", health), pb: 0.5, "reward": -10.0
                },
                {
                    st: ("C", mat, arrow, state, health), pb: 0.5, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "D", health), pb: 0.5, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.5, "reward": -10.0
                }
            ]
    if pos == "E":
        if state == "D":
            actions[ita(6)] = [
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.16, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.64, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, "R", max(0, health-50)), pb: 0.04, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, max(0, health-50)), pb: 0.16, "reward": -10.0
                }
            ]
            if arrow > 0:
                actions[ita(5)] = [
                    {
                        st: (pos, mat, arrow-1, "R", health), pb: 0.02, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, health), pb: 0.08, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, "R", max(0, health-25)), pb: 0.18, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, max(0, health-25)), pb: 0.72, "reward": -10.0
                    }
                ]
            actions[ita(1)] = [
                {
                    st: ("C", mat, arrow, "R", health), pb: 0.2, "reward": -10.0
                },
                {
                    st: ("C", mat, arrow, state, health), pb: 0.8, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.2, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.8, "reward": -10.0
                }
            ]
        else:
            actions[ita(6)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: (pos, mat, arrow, state, max(0, health-50)), pb: 0.1, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.4, "reward": -10.0
                }
            ]
            if arrow > 0:
                actions[ita(5)] = [
                    {
                        st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, max(0, health-25)), pb: 0.45, "reward": -10.0
                    },
                    {
                        st: (pos, mat, arrow-1, state, health), pb: 0.05, "reward": -10.0
                    }
                ]
            actions[ita(1)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: ("C", mat, arrow, state, health), pb: 0.5, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, 0, "D", min(accepted_health[-1], health+25)), pb: 0.5, "reward": -10.0 + -40.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.5, "reward": -10.0
                }
            ]
    if pos == "N":
        if state == "D":
            if mat > 0:
                matt = mat - 1
                actions[ita(7)] = [
                    {
                        st: (pos, matt, min(arrow+1, accepted_arrows[-1]), "R", health), pb: 0.1, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+1, accepted_arrows[-1]), state, health), pb: 0.4, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+2, accepted_arrows[-1]), "R", health), pb: 0.07, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+2, accepted_arrows[-1]), state, health), pb: 0.28, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+3, accepted_arrows[-1]), "R", health), pb: 0.03, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+3, accepted_arrows[-1]), state, health), pb: 0.12, "reward": -10.0
                    }
                ]
            actions[ita(2)] = [
                {
                    st: ("C", mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: ("C", mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
        else:
            if mat > 0:
                matt = mat-1
                actions[ita(7)] = [
                    {
                        st: (pos, matt, min(arrow+1, accepted_arrows[-1]), "D", health), pb: 0.25, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+1, accepted_arrows[-1]), state, health), pb: 0.25, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+2, accepted_arrows[-1]), "D", health), pb: 0.175, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+2, accepted_arrows[-1]), state, health), pb: 0.175, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+3, accepted_arrows[-1]), "D", health), pb: 0.075, "reward": -10.0
                    },
                    {
                        st: (pos, matt, min(arrow+3, accepted_arrows[-1]), state, health), pb: 0.075, "reward": -10.0
                    }
                ]
            actions[ita(2)] = [
                {
                    st: ("C", mat, arrow, "D", health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("C", mat, arrow, state, health),  pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "D", health), pb: 0.075, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "D", health), pb: 0.425, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "D", health), pb: 0.075, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
    if pos == "S":
        if state == "D":
            actions[ita(0)] = [
                {
                    st: ("C", mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: ("C", mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
            actions[ita(8)] = [
                {
                    st: (pos, min(mat+1, accepted_materials[-1]), arrow, "R", health), pb: 0.15, "reward": -10.0
                },
                {
                    st: (pos, min(mat+1, accepted_materials[-1]), arrow, state, health), pb: 0.6, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.05, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.2, "reward": -10.0
                },
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "R", health), pb: 0.17, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.68, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "R", health), pb: 0.03, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.12, "reward": -10.0
                }
            ]
        else:
            actions[ita(0)] = [
                {
                    st: ("C", mat, arrow, "D", health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("C", mat, arrow, state, health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "D", health), pb: 0.075, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
            actions[ita(8)] = [
                {
                    st: (pos, min(mat+1, accepted_materials[-1]), arrow, "D", health), pb: 0.375, "reward": -10.0
                },
                {
                    st: (pos, min(mat+1, accepted_materials[-1]), arrow, state, health), pb: 0.375, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, "D", health), pb: 0.125, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.125, "reward": -10.0
                },
            ]
            actions[ita(4)] = [
                {
                    st: (pos, mat, arrow, "D", health), pb: 0.425, "reward": -10.0
                },
                {
                    st: (pos, mat, arrow, state, health), pb: 0.425, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, "D", health), pb: 0.075, "reward": -10.0
                },
                {
                    st: ("E", mat, arrow, state, health), pb: 0.075, "reward": -10.0
                }
            ]
    return actions


states = []

class State:
    def __init__(self, pos, mat, arrow, state, health):
        logging.info('state initialized')
        if not pos in accepted_positions or not mat in accepted_materials or not arrow in accepted_arrows or not state in accepted_states or not health in accepted_health:
            raise SystemError
        self.pos, self.mat, self.arrow, self.state, self.health, self.policy = (pos, mat, arrow, state, health, None)
        self.set_tuple()
        self.set_index()

    it = 0
    def set_tuple(self):
        self.list = [self.pos, self.mat, self.arrow, self.state, self.health]
        self.tuple = tuple(self.list)
        it = 0

    def set_index(self):
        self.index = accepted_health.index(self.health) * 1
        val = len(accepted_health)
        self.index = self.index + accepted_states.index(self.state) * val
        val = val*len(accepted_states)
        self.index = self.index + accepted_arrows.index(self.arrow) * val
        val = val*len(accepted_arrows)
        self.index = self.index + accepted_materials.index(self.mat) * val
        val = val*len(accepted_materials)
        self.index = self.index + accepted_positions.index(self.pos) * val

    def set_actions(self):
        i = 0
        self.actions = get_actions(self.pos, self.mat, self.arrow,self.state, self.health)
        move = self.actions.keys()
        for j in move:
            for result in self.actions[j]:
                i = find_state(result[st])
                result[st] = i


class LP:
    def __init__(self):
        logging.info('setting dimension')
        self.setDimension()
        logging.info('setting matrix r')
        self.setMat_r()
        logging.info('setting matrix a')
        self.setMat_a()
        logging.info('setting alpha')
        self.setMat_alpha()
        logging.info('setting x')
        self.setVar_x()
        logging.info('setting policy')
        self.setPolicy()

    def setDimension(self):
        self.dim = 0
        for state in states:
            self.dim = self.dim + len(state.actions.keys())
    def setMat_a(self):
        idx = '0'
        idx=int(idx)
        self.a = np.zeros((600, self.dim), dtype=np.float_)
        for state in states:
            for action, results in state.actions.items():
                if action == ita(9):
                    self.a[state.index][idx] = self.a[state.index][idx] + 1.0
                else:
                    for result in results:
                        self.a[state.index][idx] = self.a[state.index][idx] + result[pb]
                        self.a[result[st].index][idx] = self.a[result[st].index][idx] - result[pb]
                idx = idx + 1

    def setMat_r(self):
        idx = '0'
        idx=int(idx)
        self.r = np.zeros((1, self.dim), dtype=np.float_)
        for state in states:
            for action, results in state.actions.items():
                for result in results:
                    self.r[0][idx] = self.r[0][idx] + result[pb] * result["reward"]
                idx = idx + 1

    def setMat_alpha(self):
        self.alpha = np.zeros((600, 1), dtype=np.float_)
        self.alpha[599] = 1.0
        it = 0

    def setVar_x(self):
        it = 0
        x = cp.Variable((self.dim, 1), 'x')
        c1  = cp.matmul(self.a, x) == self.alpha
        c2 = (0 <= x)
        constraints = [c1, c2]
        objective = cp.Maximize(cp.matmul(self.r, x))
        it += 1
        problem = cp.Problem(objective, constraints)
        self.objective = problem.solve()
        it = problem
        self.x = [float(i) for i in list(x.value)]

    def setPolicy(self):
        for state in states:
            L1 = list(state.actions.keys())
            len1 = len(state.actions.keys())
            best_action, state.policy = (L1)[np.argmax(self.x[0:len1])], (L1)[np.argmax(self.x[0:len1])]
        self.policy = [[state.tuple, state.policy] for state in states]
        idx = '0'
        idx=int(idx)

    def parse_output(self):
        os.mkdir("outputs")
        file_name = f"./outputs/part_3_output.json"
        alis = self.a.tolist()
        rlis = [float(x) for x in np.transpose(self.r)]
        alphalis = [float(x) for x in self.alpha]
        output = { "a": alis,"r": rlis,"alpha": alphalis ,"x": self.x,"policy": self.policy,"objective": float(self.objective)}
        with open(file_name, "w+") as f:
            f.write(json.dumps(output, indent=4))

        self.done = 1

def generate_states():
    for pos in range(0, 5):
        for mat in range(0, 3):
            for arrow in range(0, 4):
                for state in range(0, 2):
                    for health in range(0, 5):
                        states.append(State(accepted_positions[pos], accepted_materials[mat], accepted_arrows[arrow], accepted_states[state], accepted_health[health]))


def find_state(state_tuple):
    sid = 4
    idx = accepted_health.index(state_tuple[sid])
    val = len(accepted_health)
    sid -= 1
    idx = idx + accepted_states.index(state_tuple[sid]) * val
    val = val*len(accepted_states)
    sid -= 1
    idx = idx + accepted_arrows.index(state_tuple[sid]) * val
    val = val*len(accepted_arrows)
    sid -= 1
    idx = idx + accepted_materials.index(state_tuple[sid]) * val
    val = val*len(accepted_materials)
    sid -= 1
    idx = idx + accepted_positions.index(state_tuple[sid]) * val
    return states[idx]


generate_states()
for state in states:
    state.set_actions()

lp = LP()
lp.parse_output()
