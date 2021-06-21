import numpy as np
import cvxpy as cp
import os
import json
os.makedirs(os.path.dirname("./outputs/"), exist_ok=True)

arr = [0.5, 1.0, 2.0]
teamNum = 19

MM_attack_reward = -40.0
shoot_hp = 25
hit_hp = 50
regain_hp = 25
stepCost = -10.0 / arr[teamNum % 3]
totStates = 600
stay_cost = stepCost

acceptedArrows = [0, 1, 2, 3]
acceptedMat = [0, 1, 2]
acceptedStates = ["D", "R"]
acceptedPos = ["W", "N", "E", "S", "C"]
acceptedHealth = [0, 25, 50, 75, 100]


def getActions(pos, mat, arrow, state, health):
    actions = {}
    if health == 0:
        actions["NONE"] = []
        actions["NONE"].append({
            "probability": 1.0,
            "state": (pos, mat, arrow, state, health),
            "reward": 0.0
        })
        return actions
    elif health != 0:
        if pos == "C":
            if state == "D":
                actions["HIT"] = []
                actions["HIT"].append({  # blade
                    "probability": 0.18,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["HIT"].append({
                    "probability": 0.72,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stepCost
                })
                stateHealthVal = max(0, health-50)
                actions["HIT"].append({
                    "probability": 0.02,
                    "state": (pos, mat, arrow, "R", stateHealthVal),
                    "reward": stepCost
                })
                actions["HIT"].append({
                    "probability": 0.08,
                    "state": (pos, mat, arrow, state, stateHealthVal),
                    "reward": stepCost
                })

                if arrow >= 1:
                    actions["SHOOT"] = []
                    actions["SHOOT"].append({
                        "probability": 0.1,
                        "state": (pos, mat, arrow-1, "R", health),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.4,
                        "state": (pos, mat, arrow-1, state, health),
                        "reward": stepCost
                    })
                    stateHealthVal = max(0, health-25)
                    actions["SHOOT"].append({
                        "probability": 0.1,
                        "state": (pos, mat, arrow-1, "R", stateHealthVal),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.4,
                        "state": (pos, mat, arrow-1, state, stateHealthVal),
                        "reward": stepCost
                    })

                # left
                actions["LEFT"] = []
                actions["LEFT"].append({
                    "probability": 0.17,
                    "state": ("W", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["LEFT"].append({
                    "probability": 0.68,
                    "state": ("W", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["LEFT"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["LEFT"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                # right
                actions["RIGHT"] = []
                actions["RIGHT"].append({
                    "probability": 0.2,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["RIGHT"].append({
                    "probability": 0.8,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                # up
                actions["UP"] = []
                actions["UP"].append({
                    "probability": 0.17,
                    "state": ("N", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.68,
                    "state": ("N", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                # down
                actions["DOWN"] = []
                actions["DOWN"].append({
                    "probability": 0.17,
                    "state": ("S", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.68,
                    "state": ("S", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                # stay
                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.17,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.68,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stay_cost
                })

            elif state == "R":
                actions["HIT"] = []
                actions["HIT"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stepCost + MM_attack_reward
                })
                stateHealthVal = max(0, health-50)
                actions["HIT"].append({
                    "probability": 0.05,
                    "state": (pos, mat, arrow, state, stateHealthVal),
                    "reward": stepCost
                })
                actions["HIT"].append({
                    "probability": 0.45,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stepCost
                })

                if arrow >= 1:
                    actions["SHOOT"] = []
                    actions["SHOOT"].append({
                        "probability": 0.5,
                        "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                        "reward": stepCost + MM_attack_reward
                    })
                    stateHealthVal = max(0, health-25)
                    actions["SHOOT"].append({
                        "probability": 0.25,
                        "state": (pos, mat, arrow-1, state, stateHealthVal),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.25,
                        "state": (pos, mat, arrow-1, state, health),
                        "reward": stepCost
                    })

                actions["LEFT"] = []
                actions["LEFT"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stepCost + MM_attack_reward
                })
                actions["LEFT"].append({
                    "probability": 0.425,
                    "state": ("W", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["LEFT"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["RIGHT"] = []
                actions["RIGHT"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stepCost + MM_attack_reward
                })
                actions["RIGHT"].append({
                    "probability": 0.5,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["UP"] = []
                actions["UP"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stepCost + MM_attack_reward
                })
                actions["UP"].append({
                    "probability": 0.425,
                    "state": ("N", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["DOWN"] = []
                actions["DOWN"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stepCost + MM_attack_reward
                })
                actions["DOWN"].append({
                    "probability": 0.425,
                    "state": ("S", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stay_cost + MM_attack_reward
                })
                actions["STAY"].append({
                    "probability": 0.425,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stay_cost
                })

        elif pos == "W":
            if state == "D":
                if arrow >= 1:
                    actions["SHOOT"] = []
                    actions["SHOOT"].append({
                        "probability": 0.15,
                        "state": (pos, mat, arrow-1, "R", health),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.6,
                        "state": (pos, mat, arrow-1, state, health),
                        "reward": stepCost
                    })
                    stateHealthVal = max(0, health-25)
                    actions["SHOOT"].append({
                        "probability": 0.05,
                        "state": (pos, mat, arrow-1, "R", stateHealthVal),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.2,
                        "state": (pos, mat, arrow-1, state, stateHealthVal),
                        "reward": stepCost
                    })

                actions["RIGHT"] = []
                actions["RIGHT"].append({
                    "probability": 0.2,
                    "state": ("C", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["RIGHT"].append({
                    "probability": 0.8,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.2,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.8,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })

            elif state == "R":
                if arrow >= 1:
                    actions["SHOOT"] = []
                    actions["SHOOT"].append({
                        "probability": 0.375,
                        "state": (pos, mat, arrow-1, "D", health),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.375,
                        "state": (pos, mat, arrow-1, state, health),
                        "reward": stepCost
                    })
                    stateHealthVal = max(0, health-25)
                    actions["SHOOT"].append({
                        "probability": 0.125,
                        "state": (pos, mat, arrow-1, "D", stateHealthVal),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.125,
                        "state": (pos, mat, arrow-1, state, stateHealthVal),
                        "reward": stepCost
                    })

                actions["RIGHT"] = []
                actions["RIGHT"].append({
                    "probability": 0.5,
                    "state": ("C", mat, arrow, "D", health),
                    "reward": stepCost
                })
                actions["RIGHT"].append({
                    "probability": 0.5,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.5,
                    "state": (pos, mat, arrow, "D", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.5,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })

        elif pos == "E":
            if state == "D":
                actions["HIT"] = []
                actions["HIT"].append({
                    "probability": 0.16,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["HIT"].append({
                    "probability": 0.64,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stepCost
                })
                stateHealthVal = max(0, health-50)
                actions["HIT"].append({
                    "probability": 0.04,
                    "state": (pos, mat, arrow, "R", stateHealthVal),
                    "reward": stepCost
                })
                actions["HIT"].append({
                    "probability": 0.16,
                    "state": (pos, mat, arrow, state, stateHealthVal),
                    "reward": stepCost
                })

                if arrow >= 1:
                    actions["SHOOT"] = []
                    actions["SHOOT"].append({
                        "probability": 0.02,
                        "state": (pos, mat, arrow-1, "R", health),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.08,
                        "state": (pos, mat, arrow-1, state, health),
                        "reward": stepCost
                    })
                    stateHealthVal = max(0, health-25)
                    actions["SHOOT"].append({
                        "probability": 0.18,
                        "state": (pos, mat, arrow-1, "R", stateHealthVal),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.72,
                        "state": (pos, mat, arrow-1, state, stateHealthVal),
                        "reward": stepCost
                    })

                actions["LEFT"] = []
                actions["LEFT"].append({
                    "probability": 0.2,
                    "state": ("C", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["LEFT"].append({
                    "probability": 0.8,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.2,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.8,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })

            elif state == "R":
                actions["HIT"] = []
                actions["HIT"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stepCost + MM_attack_reward
                })
                stateHealthVal = max(0, health-50)
                actions["HIT"].append({
                    "probability": 0.1,
                    "state": (pos, mat, arrow, state, stateHealthVal),
                    "reward": stepCost
                })
                actions["HIT"].append({
                    "probability": 0.4,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stepCost
                })

                if arrow >= 1:
                    actions["SHOOT"] = []
                    actions["SHOOT"].append({
                        "probability": 0.5,
                        "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                        "reward": stepCost + MM_attack_reward
                    })
                    stateHealthVal = max(0, health-25)
                    actions["SHOOT"].append({
                        "probability": 0.45,
                        "state": (pos, mat, arrow-1, state, stateHealthVal),
                        "reward": stepCost
                    })
                    actions["SHOOT"].append({
                        "probability": 0.05,
                        "state": (pos, mat, arrow-1, state, health),
                        "reward": stepCost
                    })

                actions["LEFT"] = []
                actions["LEFT"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stepCost + MM_attack_reward
                })
                actions["LEFT"].append({
                    "probability": 0.5,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.5,
                    "state": (pos, mat, 0, "D", min(acceptedHealth[-1], health+regain_hp)),
                    "reward": stay_cost + MM_attack_reward
                })
                actions["STAY"].append({
                    "probability": 0.5,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })

        elif pos == "N":
            if state == "D":
                if mat >= 1:
                    actions["CRAFT"] = []
                    actions["CRAFT"].append({
                        "probability": 0.1,
                        "state": (pos, mat-1, min(arrow+1, acceptedArrows[-1]), "R", health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.4,
                        "state": (pos, mat-1, min(arrow+1, acceptedArrows[-1]), state, health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.07,
                        "state": (pos, mat-1, min(arrow+2, acceptedArrows[-1]), "R", health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.28,
                        "state": (pos, mat-1, min(arrow+2, acceptedArrows[-1]), state, health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.03,
                        "state": (pos, mat-1, min(arrow+3, acceptedArrows[-1]), "R", health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.12,
                        "state": (pos, mat-1, min(arrow+3, acceptedArrows[-1]), state, health),
                        "reward": stepCost
                    })

                actions["DOWN"] = []
                actions["DOWN"].append({
                    "probability": 0.17,
                    "state": ("C", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.68,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.17,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.68,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stay_cost
                })

            elif state == "R":
                if mat >= 1:
                    actions["CRAFT"] = []
                    actions["CRAFT"].append({
                        "probability": 0.25,
                        "state": (pos, mat-1, min(arrow+1, acceptedArrows[-1]), "D", health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.25,
                        "state": (pos, mat-1, min(arrow+1, acceptedArrows[-1]), state, health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.175,
                        "state": (pos, mat-1, min(arrow+2, acceptedArrows[-1]), "D", health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.175,
                        "state": (pos, mat-1, min(arrow+2, acceptedArrows[-1]), state, health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.075,
                        "state": (pos, mat-1, min(arrow+3, acceptedArrows[-1]), "D", health),
                        "reward": stepCost
                    })
                    actions["CRAFT"].append({
                        "probability": 0.075,
                        "state": (pos, mat-1, min(arrow+3, acceptedArrows[-1]), state, health),
                        "reward": stepCost
                    })

                actions["DOWN"] = []
                actions["DOWN"].append({
                    "probability": 0.425,
                    "state": ("C", mat, arrow, "D", health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.425,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, "D", health),
                    "reward": stepCost
                })
                actions["DOWN"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.425,
                    "state": (pos, mat, arrow, "D", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.425,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, "D", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stay_cost
                })

        elif pos == "S":
            if state == "D":
                actions["UP"] = []
                actions["UP"].append({
                    "probability": 0.17,
                    "state": ("C", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.68,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["GATHER"] = []
                stateMatVal = min(mat+1, acceptedMat[-1])
                actions["GATHER"].append({
                    "probability": 0.15,
                    "state": (pos, stateMatVal, arrow, "R", health),
                    "reward": stepCost
                })
                actions["GATHER"].append({
                    "probability": 0.6,
                    "state": (pos, stateMatVal, arrow, state, health),
                    "reward": stepCost
                })
                actions["GATHER"].append({
                    "probability": 0.05,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stepCost
                })
                actions["GATHER"].append({
                    "probability": 0.2,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.17,
                    "state": (pos, mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.68,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.03,
                    "state": ("E", mat, arrow, "R", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.12,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stay_cost
                })

            elif state == "R":
                actions["UP"] = []
                actions["UP"].append({
                    "probability": 0.425,
                    "state": ("C", mat, arrow, "D", health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.425,
                    "state": ("C", mat, arrow, state, health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, "D", health),
                    "reward": stepCost
                })
                actions["UP"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["GATHER"] = []
                stateMatVal = min(mat+1, acceptedMat[-1])
                actions["GATHER"].append({
                    "probability": 0.375,
                    "state": (pos, stateMatVal, arrow, "D", health),
                    "reward": stepCost
                })
                actions["GATHER"].append({
                    "probability": 0.375,
                    "state": (pos, stateMatVal, arrow, state, health),
                    "reward": stepCost
                })
                actions["GATHER"].append({
                    "probability": 0.125,
                    "state": (pos, mat, arrow, "D", health),
                    "reward": stepCost
                })
                actions["GATHER"].append({
                    "probability": 0.125,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stepCost
                })

                actions["STAY"] = []
                actions["STAY"].append({
                    "probability": 0.425,
                    "state": (pos, mat, arrow, "D", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.425,
                    "state": (pos, mat, arrow, state, health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, "D", health),
                    "reward": stay_cost
                })
                actions["STAY"].append({
                    "probability": 0.075,
                    "state": ("E", mat, arrow, state, health),
                    "reward": stay_cost
                })
        return actions


states = []


class State:
    def __init__(self, pos, mat, arrow, state, health):
        self.mat = mat
        self.pos = pos
        self.policy = None
        self.state = state
        self.arrow = arrow
        self.health = health
        self.setIndex()
        self.tuple = (self.pos, self.mat, self.arrow, self.state, self.health)

    def fun1(self):
        for move in self.actions:
            for i in range(len(self.actions[move])):
                self.actions[move][i]["state"] = find_state(self.actions[move][i]["state"])

    def setActions(self):
        self.actions = getActions(self.pos, self.mat, self.arrow,
                                  self.state, self.health)
        self.fun1()

    def setIndex(self):
        healthV = self.health
        stateV = self.state
        arrowV = self.arrow
        matV = self.mat
        posV = self.pos
        val = 1

        healthL = len(acceptedHealth)
        stateL = len(acceptedStates)
        arrowL = len(acceptedArrows)
        matL = len(acceptedMat)
        self.index = acceptedHealth.index(healthV) * val
        val *= healthL
        self.index += acceptedStates.index(stateV) * val
        val *= stateL
        self.index += acceptedArrows.index(arrowV) * val
        val *= arrowL
        self.index += acceptedMat.index(matV) * val
        val *= matL
        self.index += acceptedPos.index(posV) * val


def createActions():
    for i in range(len(states)):
        states[i].setActions()


class LP:
    def __init__(self):
        self.dim = 0
        self.setDimension()
        self.aSetMat()
        self.rSetMat()
        self.alphaSetMat()
        self.setVar_x()
        self.setPolicy()

    def setDimension(self):
        for i in range(len(states)):
            self.dim = self.dim + len(states[i].actions.keys())

    def aSetMat(self):
        idx = 0
        self.a = np.zeros((totStates, self.dim), dtype=np.float_)
        for tem in range(len(states)):
            i = states[tem].index
            for action, results in states[tem].actions.items():
                if action == "NONE":
                    self.a[i][idx] += 1.0
                elif action != "NONE":
                    for temr in range(len(results)):
                        self.a[i][idx] += results[temr]["probability"]
                        self.a[results[temr]["state"].index][idx] -= results[temr]["probability"]
                idx = idx + 1

    def setVar_x(self):
        charc = 'x'
        x = cp.Variable((self.dim, 1), charc)
        constraints = [cp.matmul(self.a, x) == self.alpha, x >= 0]
        objective = cp.Maximize(cp.matmul(self.r, x))
        prob = cp.Problem(objective, constraints)
        soln = prob.solve()
        self.objective = soln
        self.x = [float(kk) for kk in list(x.value)]

    def rSetMat(self):
        idx = 0
        self.r = np.zeros((1, self.dim), dtype=np.float_)
        for tem in range(len(states)):
            i = states[tem].index
            for action, results in states[tem].actions.items():
                for temr in range(len(results)):
                    self.r[0][idx] += results[temr]["probability"] * results[temr]["reward"]
                idx = idx + 1

    def alphaSetMat(self):
        self.alpha = np.zeros((totStates, 1), dtype=np.float_)
        numV = totStates-1
        self.alpha[numV] = 1.0

    def setPolicy(self):
        idx = 0
        for tem in range(len(states)):
            best_action = list(states[tem].actions.keys())[np.argmax(
                self.x[idx:idx+len(states[tem].actions.keys())])]
            states[tem].policy = best_action
        self.policy = [[states[kk].tuple, states[kk].policy] for kk in range(len(states))]

    def parseOutput(self):
        file_name = "./outputs/part_3_output.json"
        aVal = self.a.tolist()
        rVal = [float(x) for x in np.transpose(self.r)]
        alphaVal = [float(x) for x in self.alpha]
        xVal = self.x
        policyVal = self.policy
        objectiveVal = float(self.objective)
        self.output = {
            "a": aVal,
            "r": rVal,
            "alpha": alphaVal,
            "x": xVal,
            "policy": policyVal,
            "objective": objectiveVal
        }
        with open(file_name, "w+") as f:
            f.write(json.dumps(self.output, indent=4))


def find_state(state_tuple):
    val = 1
    healthV = state_tuple[4]
    stateV = state_tuple[3]
    arrowV = state_tuple[2]
    matV = state_tuple[1]
    posV = state_tuple[0]

    healthL = len(acceptedHealth)
    stateL = len(acceptedStates)
    arrowL = len(acceptedArrows)
    matL = len(acceptedMat)

    idx = acceptedHealth.index(healthV) * val
    val *= healthL
    idx += acceptedStates.index(stateV) * val
    val *= stateL
    idx += acceptedArrows.index(arrowV) * val
    val *= arrowL
    idx += acceptedMat.index(matV) * val
    val *= matL
    idx += acceptedPos.index(posV) * val
    return states[idx]


# main
for ind1 in range(len(acceptedPos)):
    for ind2 in range(len(acceptedMat)):
        for ind3 in range(len(acceptedArrows)):
            for ind4 in range(len(acceptedStates)):
                for ind5 in range(len(acceptedHealth)):
                    states.append(State(acceptedPos[ind1], acceptedMat[ind2], acceptedArrows[ind3], acceptedStates[ind4], acceptedHealth[ind5]))

createActions()


lp = LP()
lp.parseOutput()
