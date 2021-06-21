import cvxpy as cp
import json
import os
import numpy as np


valid_positions = ["W", "N", "E", "S", "C"]
m1,m2,m3=0,1,2
valid_materials=[0,1,2]
ar1,ar2,ar3,ar4=0,1,2,3
valid_arrows = [0, 1, 2, 3]
s1,s2="D","R"#Dormant state, Ready state
valid_states = ["D", "R"]
hl1,hl2,hl3,hl4,hl5=0,25,50,75,100
valid_health = [0, 25, 50, 75, 100]
totalStates=600
states = []
mat_alp = np.zeros((totalStates, 1), dtype=np.float_)
policy_list=[]
arr_x=[]

def create_dictonary(cols,solved_obj,mat_a,mat_r,arr_x,policy_list):
    dicto = {
            "a": mat_a.tolist(),
            "r": [float(x) for x in np.transpose(mat_r)],
            "alpha": [float(x) for x in mat_alp],
            "x": arr_x,
            "policy": policy_list,
            "objective": float(solved_obj)
        }
    if(os.path.exists("./outputs")):
        open('./outputs/part_3_output.json', 'w').close()   
    else:
        os.mkdir("./outputs")

    with open('./outputs/part_3_output.json', 'w') as file:
        file.write(json.dumps(dicto, indent=4))

def get_valid_act(position, material, arrow, state, health,scost,attack_rew,gain_health):
    is_action = dict()
    as_it_is = (position, material, arrow, state, health)
    dormant_as_it_is = (position, material, arrow,"D", health)
    ready_as_it_is = (position, material, arrow, valid_states[1], health)
    if health == 0:
        is_action["NONE"] = [
            {
                "p": 1.0,
                "s": as_it_is,
                "rew": 0.0
            }
        ]
        return is_action

    min_strong=min(100,health+gain_health)#porb 0.5
    strong_reward = scost + attack_rew
    half_enemy=health-50 #prob 0.05
    max_half=max(0,half_enemy)
    pav_enemy=health-25 #prob 0.25
    max_pav=max(0,pav_enemy)
    min_strong_tuple=(position, material, 0, valid_states[0], min_strong)
    dec_arrow_tuple=(position, material, arrow-1, state, health)
    dec_arpav_tuple=(position, material, arrow-1, state, max_pav)
    # arsd dec arrow set dormant state
    half_as_it_is = (position, material, arrow, state, max_half)
    north_set_as_it_is = (valid_positions[2], material, arrow, state, health)
    if position == valid_positions[4]:
        if state == valid_states[0]: #Dormat state
            is_action["HIT"] = [
                {
                    "p": 0.18,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.72,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.02,
                    "s": (position, material, arrow, valid_states[1], max_half),
                    "rew": scost
                },
                {
                    "p": 0.08,
                    "s": half_as_it_is,
                    "rew": scost
                }
            ]
            if arrow > 0:
                dec_arsd_tuple= (position, material, arrow-1, valid_states[1], health)
                is_action["SHOOT"] = [
                    {
                        "p": 0.1,
                        "s": dec_arsd_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.4,
                        "s": dec_arrow_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.1,
                        "s": (position, material, arrow-1, valid_states[1], max_pav),
                        "rew": scost
                    },
                    {
                        "p": 0.4,
                        "s": dec_arpav_tuple,
                        "rew": scost
                    }
                ]
            is_action["LEFT"] = [
                {
                    "p": 0.17,
                    "s": (valid_positions[0], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": (valid_positions[0], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["RIGHT"] = [
                {
                    "p": 0.2,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.8,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["UP"] = [
                {
                    "p": 0.17,
                    "s": (valid_positions[1], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": (valid_positions[1], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["DOWN"] = [
                {
                    "p": 0.17,
                    "s": (valid_positions[3], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": (valid_positions[3], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.17,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
        else:
            is_action["HIT"] = [
                {
                    "p": 0.5,
                    "s": min_strong_tuple,
                    "rew": strong_reward
                },
                {
                    "p": 0.05,
                    "s": half_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.45,
                    "s": as_it_is,
                    "rew": scost
                }
            ]
            if arrow > 0:
                dec_pav_tuple=(position, material, arrow-1, state,max_pav)
                is_action["SHOOT"] = [
                    {
                        "p": 0.5,
                        "rew": strong_reward,
                        "s": min_strong_tuple,
                    },
                    {
                        "p": 0.25,
                        "s": dec_pav_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.25,
                        "s": dec_arrow_tuple,
                        "rew": scost
                    }
                ]
            is_action["LEFT"] = [
                {
                    "p": 0.5,
                    "s": (position, material, 0, valid_states[0],min_strong),
                    "rew": strong_reward
                },
                {
                    "p": 0.425,
                    "s": (valid_positions[0], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["RIGHT"] = [
                {
                    "p": 0.5,
                    "s": min_strong_tuple,
                    "rew": strong_reward
                },
                {
                    "p": 0.5,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["UP"] = [
                {
                    "p": 0.5,
                    "s": min_strong_tuple,
                    "rew": strong_reward
                },
                {
                    "p": 0.425,
                    "s": (valid_positions[1], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["DOWN"] = [
                {
                    "p": 0.5,
                    "s": min_strong_tuple,
                    "rew": strong_reward
                },
                {
                    "p": 0.425,
                    "s": (valid_positions[3], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.5,
                    "s": (position, material, 0, valid_states[0],min_strong),
                    "rew": strong_reward
                },
                {
                    "p": 0.425,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
    if position == valid_positions[0]:
        dec_arsd_tuple= (position, material, arrow-1, valid_states[1], health)
        if state == valid_states[0]:
            if arrow > 0:
                is_action["SHOOT"] = [
                    {
                        "p": 0.15,
                        "s": dec_arsd_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.6,
                        "s": dec_arrow_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.05,
                        "s": (position, material, arrow-1, valid_states[1], max_pav),
                        "rew": scost
                    },
                    {
                        "p": 0.2,
                        "s": dec_arpav_tuple,
                        "rew": scost
                    }
                ]
            is_action["RIGHT"] = [
                {
                    "p": 0.2,
                    "s": (valid_positions[4], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.8,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.2,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.8,
                    "s": as_it_is,
                    "rew": scost
                }
            ]
        else:
            if arrow > 0:
                set_state_tuple=(position, material, arrow-1, valid_states[0], health)
                pav_state_tuple=(position, material, arrow-1, valid_states[0], max_pav)
                is_action["SHOOT"] = [
                    {
                        "p": 0.375,
                        "s": set_state_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.375,
                        "s": dec_arrow_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.125,
                        "s": pav_state_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.125,
                        "s": dec_arpav_tuple,
                        "rew": scost
                    }
                ]
            is_action["RIGHT"] = [
                {
                    "p": 0.5,
                    "s": (valid_positions[4], material, arrow, valid_states[0], health),
                    "rew": scost
                },
                {
                    "p": 0.5,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.5,
                    "s": dormant_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.5,
                    "s": as_it_is,
                    "rew": scost
                }
            ]
    if position== valid_positions[2]:
        if state == valid_states[0]:
            is_action["HIT"] = [
                {
                    "p": 0.16,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.64,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.04,
                    "s": (position, material, arrow, valid_states[1], max_half),
                    "rew": scost
                },
                {
                    "p": 0.16,
                    "s": half_as_it_is,
                    "rew": scost
                }
            ]
            if arrow > 0:
                dec_arsd_tuple= (position, material, arrow-1, valid_states[1], health)
                is_action["SHOOT"] = [
                    {
                        "p": 0.02,
                        "s": dec_arsd_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.08,
                        "s": dec_arrow_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.18,
                        "s": (position, material, arrow-1, valid_states[1], max_pav),
                        "rew": scost
                    },
                    {
                        "p": 0.72,
                        "s": dec_arpav_tuple,
                        "rew": scost
                    }
                ]
            is_action["LEFT"] = [
                {
                    "p": 0.2,
                    "s": (valid_positions[4], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.8,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.2,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.8,
                    "s": as_it_is,
                    "rew": scost
                }
            ]
        else:
            is_action["HIT"] = [
                {
                    "p": 0.5,
                    "s": min_strong_tuple,
                    "rew": strong_reward
                },
                {
                    "p": 0.1,
                    "s": half_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.4,
                    "s": as_it_is,
                    "rew": scost
                }
            ]
            if arrow > 0:
                is_action["SHOOT"] = [
                    {
                        "p": 0.5,
                        "rew": strong_reward,
                        "s": min_strong_tuple,
                    },
                    {
                        "p": 0.45,
                        "s": dec_arpav_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.05,
                        "s": dec_arrow_tuple,
                        "rew": scost
                    }
                ]
            is_action["LEFT"] = [
                {
                    "p": 0.5,
                    "s": min_strong_tuple,
                    "rew": strong_reward
                },
                {
                    "p": 0.5,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.5,
                    "s": min_strong_tuple,
                    "rew": strong_reward
                },
                {
                    "p": 0.5,
                    "s": as_it_is,
                    "rew": scost
                }
            ]
    if position== valid_positions[1]:
        set_crsr_tuple = (position, material-1, min(arrow+1, ar4), valid_states[1], health) #craft and set ready state
        if state == valid_states[0]:
            if material> 0:
                is_action["CRAFT"] = [
                    {
                        "p": 0.1,
                        "s": set_crsr_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.4,
                        "s": (position, material-1, min(arrow+1, ar4), state, health),
                        "rew": scost
                    },
                    {
                        "p": 0.07,
                        "s": (position, material-1, min(arrow+2, ar4), valid_states[1], health),
                        "rew": scost
                    },
                    {
                        "p": 0.28,
                        "s": (position, material-1, min(arrow+2, ar4), state, health),
                        "rew": scost
                    },
                    {
                        "p": 0.03,
                        "s": (position, material-1, min(arrow+3, ar4), valid_states[1], health),
                        "rew": scost
                    },
                    {
                        "p": 0.12,
                        "s": (position, material-1, min(arrow+3, ar4), state, health),
                        "rew": scost
                    }
                ]
            is_action["DOWN"] = [
                {
                    "p": 0.17,
                    "s": (valid_positions[4], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.17,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
        else:
            set_crsd_tuple= (position, material-1, min(arrow+1, ar4), valid_states[0], health) #craft and set dormant state
            if material> 0:
                is_action["CRAFT"] = [
                    {
                        "p": 0.25,
                        "s": set_crsd_tuple,
                        "rew": scost
                    },
                    {
                        "p": 0.25,
                        "s": (position, material-1, min(arrow+1, ar4), state, health),
                        "rew": scost
                    },
                    {
                        "p": 0.175,
                        "s": (position, material-1, min(arrow+2, ar4), valid_states[0], health),
                        "rew": scost
                    },
                    {
                        "p": 0.175,
                        "s": (position, material-1, min(arrow+2, ar4), state, health),
                        "rew": scost
                    },
                    {
                        "p": 0.075,
                        "s": (position, material-1, min(arrow+3, ar4), valid_states[0], health),
                        "rew": scost
                    },
                    {
                        "p": 0.075,
                        "s": (position, material-1, min(arrow+3, ar4), state, health),
                        "rew": scost
                    }
                ]
            is_action["DOWN"] = [
                {
                    "p": 0.425,
                    "s": (valid_positions[4], material, arrow, valid_states[0], health),
                    "rew": scost
                },
                {
                    "p": 0.425,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": (valid_positions[2], material, arrow, valid_states[0], health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["STAY"] = [
                {
                    "p": 0.425,
                    "s": dormant_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.425,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": (valid_positions[2], material, arrow, valid_states[0], health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
    if position== valid_positions[3]:
        gathered_as_it_is=(position, min(material+1, m3), arrow, state, health)
        set_gathered_tuple = (position, min(material+1, m3), arrow, valid_states[1], health)
        if state == valid_states[0]:
            is_action["UP"] = [
                {
                    "p": 0.17,
                    "s": (valid_positions[4], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["GATHER"] = [
                {
                    "p": 0.15,
                    "s": set_gathered_tuple,
                    "rew": scost
                },
                {
                    "p": 0.6,
                    "s": gathered_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.05,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.2,
                    "s": as_it_is,
                    "rew": scost
                },
            ]
            is_action["STAY"] = [
                {
                    "p": 0.17,
                    "s": ready_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.68,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.03,
                    "s": (valid_positions[2], material, arrow, valid_states[1], health),
                    "rew": scost
                },
                {
                    "p": 0.12,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
        else:
            set_gathered_tuple=(position, min(material+1, m3), arrow, valid_states[0], health)
            is_action["UP"] = [
                {
                    "p": 0.425,
                    "s": (valid_positions[4], material, arrow, valid_states[0], health),
                    "rew": scost
                },
                {
                    "p": 0.425,
                    "s": (valid_positions[4], material, arrow, state, health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": (valid_positions[2], material, arrow, valid_states[0], health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
            is_action["GATHER"] = [
                {
                    "p": 0.375,
                    "s": set_gathered_tuple,
                    "rew": scost
                },
                {
                    "p": 0.375,
                    "s": gathered_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.125,
                    "s": dormant_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.125,
                    "s": as_it_is,
                    "rew": scost
                },
            ]
            is_action["STAY"] = [
                {
                    "p": 0.425,
                    "s": dormant_as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.425,
                    "s": as_it_is,
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": (valid_positions[2], material, arrow, valid_states[0], health),
                    "rew": scost
                },
                {
                    "p": 0.075,
                    "s": north_set_as_it_is,
                    "rew": scost
                }
            ]
    return is_action

class Manage_State:
    def __init__(self, position, material, arrow, state, health):
        flg=0
        if not position in valid_positions or not material in valid_materials or not arrow in valid_arrows or not state in valid_states or not health in valid_health:
            flg=1
        if flg!=0:
            raise SystemError
      
        self.position = position
        self.attack_rew=-40.0
        self.material = material
        self.gain_health=25
        self.arrow = arrow
        self.scost=-20.0
        self.state = state
        self.cur_spolicy=None
        self.health = health      
        self.maphealth(self.health)
        self.mapstate(self.state)
        self.maparrows(self.arrow)
        self.mapmat(self.material)
        self.mappos(self.position)
        self.convert_to_tuple()
    def maphealth(self,h):
        self.temp=1
        self.mapx=valid_health.index(h) * self.temp
        self.temp*=5
    def mapstate(self,s):
        self.mapx+=valid_states.index(s) * self.temp
        self.temp*=2
    def maparrows(self,a):
        self.mapx+=valid_arrows.index(a) * self.temp
        self.temp*=4
    def mapmat(self,m):
        self.mapx+=valid_materials.index(m) * self.temp
        self.temp*=3
    def mappos(self,p):
        self.mapx+=valid_positions.index(p) * self.temp
    def convert_to_tuple(self):
        cur_pos,cur_heal=self.position,self.health
        cur_mat,cur_ar,cur=self.material,self.arrow,self.state
        self.tuple = (cur_pos, cur_mat, cur_ar, cur, cur_heal)  
    def store_acts(self):
        cur_pos,cur_heal=self.position,self.health
        cur_mat,cur_ar=self.material,self.arrow
        cur,cur_scost=self.state,self.scost
        cur_enemy_rew,cur_gainH=self.attack_rew,self.gain_health
        self.valid_acts = get_valid_act(cur_pos, cur_mat, cur_ar,
                                   cur, cur_heal,cur_scost,cur_enemy_rew,cur_gainH)
        for move in self.valid_acts:
            for result in self.valid_acts[move]:
                val=1
                ind = valid_health.index(result["s"][4]) * val
                val *= len(valid_health)
                ind += valid_states.index(result["s"][3]) * val
                val *= len(valid_states)
                ind += valid_arrows.index(result["s"][2]) * val
                val *= len(valid_arrows)
                ind += valid_materials.index(result["s"][1]) * val
                val *= len(valid_materials)
                ind += valid_positions.index(result["s"][0]) * val
                result["s"] =  states[ind]


def main():
    for p in range(0,len(valid_positions)):
        for m in range(0,len(valid_materials)):
            for a in range(0,len(valid_arrows)):
                for s in range(0,len(valid_states)):
                    for h in range(0,len(valid_health)):
                        states.append(Manage_State(valid_positions[p], valid_materials[m], valid_arrows[a], valid_states[s], valid_health[h]))
    for state in states:
        state.store_acts()
    cols,indx =0,0
    for state in states:
            cols += len(state.valid_acts.keys())
    mat_a= np.zeros((totalStates, cols), dtype=np.float_)
    mat_r = np.zeros((1,cols), dtype=np.float_)
    for state in states:
        state_act_items=state.valid_acts.items()
        for action, results in state_act_items:
            #if none prob 1.0
            if action == "NONE":
                mat_a[state.mapx][indx] += 1.0
            else:
                for result in results:
                    it,res_item=state.mapx, result["s"].mapx
                    mat_a[it][indx] += result["p"]
                    mat_a[res_item][indx] -= result["p"]
            indx += 1
    indx = 0
    for state in states:
        state_act_items=state.valid_acts.items()
        for action, results in state_act_items:
            for result in results:
                mat_r[0][indx] += result["p"] * result["rew"]
            indx += 1
    mat_alp[totalStates-1] = 1.0
    x = cp.Variable((cols, 1), 'x')
    constraints = [x >= 0,mat_a @ x == mat_alp]
    objective = cp.Maximize(mat_r @ x)
    problem = cp.Problem(objective, constraints)
    solved_obj = problem.solve()
    arr_x = [float(i) for i in list(x.value)]
    indx = 0
    for state in states:
        best_action = list(state.valid_acts.keys())[np.argmax(arr_x[indx:indx+len(state.valid_acts.keys())])]
        state.cur_spolicy = best_action
    policy_list = [[state.tuple, state.cur_spolicy] for state in states]
    create_dictonary(cols,solved_obj,mat_a,mat_r,arr_x,policy_list )

main()
