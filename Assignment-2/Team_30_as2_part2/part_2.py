import numpy as np
import os 
import sys
'''
Position 0=West
Position 1=North
Position 2=East
Position 3=South
Position 4=Centre
Action 0=Up
Action 1=Left
Action 2=DOwn
Action 3=Right
Action 4=Stay
Action 5=Shoot
Action 6=Hit
Action 7=Craft
Action 8=Gather
Action 9=None
State 0=Dormant
State 1=Active
'''
reward=0
def mapact(a):
	if(a==0):
		return "UP"
	elif(a==1):
		return "LEFT"
	elif(a==2):
		return "DOWN"
	elif(a==3):
		return "RIGHT"
	elif(a==4):
		return "STAY"
	elif(a==5):
		return "SHOOT"
	elif(a==6):
		return "HIT"
	elif(a==7):
		return "CRAFT"
	elif(a==8):
		return "GATHER"
	else:
		return "NONE"
def north(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	if(s1==0 and s2==0):
		if(act==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return(0.8*0.85)
			if(p2==2):
				return(0.8*0.15)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==1):
				return(0.8*0.85)
			if(p2==2):
				return(0.8*0.15)
		if(act==7 and m1>=1 and m2-m1==-1 and h1-h2==0):
			if(a2==1):
				return(0.5*0.8)
			if(a2==2):
				return(0.35*0.8)
			if(a2==3):
				return(0.15*0.8)	
		return 0
	if(s1==0 and s2==1):
		if(act==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return(0.2*0.85)
			if(p2==2):
				return(0.2*0.15)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==1):
				return(0.2*0.85)
			if(p2==2):
				return(0.2*0.15)
		if(act==7 and m1>=1 and m2-m1==-1 and h1-h2==0):
			if(a2==1):
				return(0.5*0.2)
			if(a2==2):
				return(0.35*0.2)
			if(a2==3):
				return(0.15*0.2)	
		return 0			
	if(s1==1 and (s2==0 or s2==1)):
		if(act==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return(0.5*0.85)
			if(p2==2):
				return(0.5*0.15)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==1):
				return(0.5*0.15)
			if(p2==2):
				return(0.5*0.15)
		if(act==7 and m1>=1 and m2-m1==-1 and h1-h2==0):
			if(a2==1):
				return(0.5*0.5)
			if(a2==2):
				return(0.35*0.5)
			if(a2==3):
				return(0.15*0.5)	
		return 0
	return 0
def south(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	if(s1==0 and s2==0):#dormant to domant
		if(act==0 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return(0.8*0.85)
			if(p2==2):
				return(0.8*0.15)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==3):
				return(0.8*0.15)
			if(p2==2):
				return(0.8*0.15)
		if(act==8 and p2==p1 and a1-a2==0 and h1-h2==0):
			if(m2-m1==1):
				return(0.8*0.75)
			if(m2-m1==0):
				return(0.8*0.25)
		return 0
	if(s1==0 and s2==1):#dormant to active
		if(act==0 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return(0.2*0.85)
			if(p2==2):
				return(0.2*0.15)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==3):
				return(0.2*0.15)
			if(p2==2):
				return(0.2*0.15)
		if(act==8 and p2==p1 and a1-a2==0 and h1-h2==0):
			if(m2-m1==1 ):
				return(0.2*0.75)
			if(m2-m1==0):
				return(0.2*0.25)
		return 0
	if(s1==1 and (s2==0 or s2==1)):#active to any other
		if(act==0 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return(0.5*0.85)
			if(p2==2):
				return(0.5*.15)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==3):
				return(0.5*0.15)
			if(p2==2):
				return(0.5*0.15)
		if(act==8 and p2==p1 and a1-a2==0 and h1-h2==0):
			if(m2-m1==1 ):
				return(0.5*0.75)
			if(m2-m1==0):
				return(0.5*0.25)
		return 0
	return 0

def west(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	if(s1==0 and s2==0):#from dormant to dormant
		if(act==3 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (1*0.8)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (1*0.8)
		if(act==5 and m1-m2==0):
			if(p2==0 and a1-a2==1 and (h2-h1==-25)):
				return(0.8*0.25)
			if(p2==0 and a1-a2==1 and (h2-h1==0)):
				return (0.8*0.75)
		return 0
	if(s1==0 and s2==0):#from dormant to active
		if(act==3 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (1*0.2)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (1*0.2)
		if(act==5 and m1-m2==0):
			if(p2==0 and a1-a2==1 and (h2-h1==-25)):
				return(0.2*0.25)
			if(p2==0 and a1-a2==1 and (h2-h1==0)):
				return (0.2*0.75)
		return 0
	if(s1==1 and (s2==1 or s2==0)):#from dormant to active
		if(act==3 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (1*0.5)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (1*0.5)
		if(act==5 and m1-m2==0):
			if(p2==0 and a1-a2==1 and (h2-h1==-25)):
				return(0.5*0.25)
			if(p2==0 and a1-a2==1 and (h2-h1==0)):
				return (0.5*0.75)
		return 0
	return 0

def east(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	global reward
	if(s1==0 and s2==0):#mm from doramnt to dormant
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (1*0.8)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==2):
				return (1*0.8)
		if(act==5 and m1-m2==0):
			if(p2==2 and (a1-a2==1) and (h2-h1==-25)):#arrow hit
				return (0.9*0.8)
			if(p2==2 and (a1-a2==1) and (h2-h1==0)):#arrow miss
				return (0.1*0.8)
		if(act==6 and m1-m2==0 and a1-a2==0):
			if(p2==2  and (h2-h1==-50)):
				return (0.2*0.8)
			if(p2==2  and (h2-h1==0)):
				return (0.8*0.8)
		return 0	
	if(s1==0 and s2==1):#mm from doramnt to active
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (1*0.2)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==2):
				return (1*0.2)
		if(act==5 and m1-m2==0):
			if(p2==2 and (a1-a2==1) and (h2-h1==-25)):#arrow hit
				return (0.9*0.2)
			if(p2==2 and (a1-a2==1) and (h2-h1==0)):#arrow miss
				return (0.1*0.2)
		if(act==6 and m1-m2==0 and a1-a2==0):
			if(p2==2  and (h2-h1==-50)):#blade hit
				return (0.2*0.2)
			if(p2==2  and (h2-h1==0)):#blade miss
				return (0.8*0.2)
		return 0
	if(s1==1 and s2==1):#mm from active to active
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (1*0.5)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==2):
				return (1*0.5)
		if(act==5 and m1-m2==0):
			if(p2==2 and (a1-a2==1) and (h2-h1==-25)):#arrow hit
				return (0.9*0.5)
			if(p2==2 and (a1-a2==1) and (h2-h1==0)):#arrow miss
				return (0.1*0.5)
		if(act==6 and a1-a2==0 and m1-m2==0):
			if(p2==2  and (h2-h1==-50)):#blade hit
				return (0.2*0.5)
			if(p2==2  and (h2-h1==0)):#blade miss
				return (0.8*0.5)
		return 0
	if(s1==1 and s2==0):#mm from active to dormant
		if(a2==0 and h2-h1==25):
			if(act==1 and m1-m2==0):#up
				if(p2==2):
					reward=reward-40
					return (1*0.5)
			if(act==4 and m1-m2==0):
				if(p2==2):
					reward=reward-40
					return (1*0.5)
			if(act==5 and m1-m2==0):
				if(p2==2 and (a1-a2==1)):#arrow miss
					reward=reward-40
					return (1*0.5)
			if(act==6 and m1-m2==0):
				if(p2==2):#blade miss
					reward=reward-40
					return (1*0.5)
			return 0
		return 0
	return 0

def east1(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	global reward
	if(s1==0 and s2==0):#mm from doramnt to dormant
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (1*0.8)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==2):
				return (1*0.8)
		if(act==5 and m1-m2==0):
			if(p2==2 and (a1-a2==1) and (h2-h1==-25)):#arrow hit
				return (0.9*0.8)
			if(p2==2 and (a1-a2==1) and (h2-h1==0)):#arrow miss
				return (0.1*0.8)
		if(act==6 and m1-m2==0 and a1-a2==0):
			if(p2==2  and (h2-h1==-50)):
				return (0.2*0.8)
			if(p2==2  and (h2-h1==0)):
				return (0.8*0.8)
		return 0	
	if(s1==0 and s2==1):#mm from doramnt to active
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (1*0.2)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==2):
				return (1*0.2)
		if(act==5 and m1-m2==0):
			if(p2==2 and (a1-a2==1) and (h2-h1==-25)):#arrow hit
				return (0.9*0.2)
			if(p2==2 and (a1-a2==1) and (h2-h1==0)):#arrow miss
				return (0.1*0.2)
		if(act==6 and m1-m2==0 and a1-a2==0):
			if(p2==2  and (h2-h1==-50)):#blade hit
				return (0.2*0.2)
			if(p2==2  and (h2-h1==0)):#blade miss
				return (0.8*0.2)
		return 0
	if(s1==1 and s2==1):#mm from active to active
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (1*0.5)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==2):
				return (1*0.5)
		if(act==5 and m1-m2==0):
			if(p2==2 and (a1-a2==1) and (h2-h1==-25)):#arrow hit
				return (0.9*0.5)
			if(p2==2 and (a1-a2==1) and (h2-h1==0)):#arrow miss
				return (0.1*0.5)
		if(act==6 and a1-a2==0 and m1-m2==0):
			if(p2==2  and (h2-h1==-50)):#blade hit
				return (0.2*0.5)
			if(p2==2  and (h2-h1==0)):#blade miss
				return (0.8*0.5)
		return 0
	if(s1==1 and s2==0):#mm from active to dormant
		if(a2==0 and h2-h1==25):
			if(act==1 and m1-m2==0):#up
				if(p2==2):
					reward=reward-40
					return (1*0.5)
			if(act==4 and m1-m2==0):
				if(p2==2):
					reward=reward-40
					return (1*0.5)
			if(act==5 and m1-m2==0):
				if(p2==2 and (a1-a2==1)):#arrow miss
					reward=reward-40
					return (1*0.5)
			if(act==6 and m1-m2==0):
				if(p2==2):#blade miss
					reward=reward-40
					return (1*0.5)
			return 0
		return 0
	return 0
def centre(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	global reward
	#reward+=2
	if(s1==0 and s2==0):#mm from doramnt to dormant
		if(act==0):
			if(p2==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.85*0.8)
			if(p2==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.15*0.8)
		if(act==1):
			if(p2==0 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.85*0.8)
			if(p2==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.15*0.8)
		if(act==2):
			if(p2==3 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.85*0.8)
			if(p2==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.15*0.8)
		if(act==3 and p2==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			return (1*0.8)
		if(act==4):
			if(p2==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.85*0.8)
			if(p2==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
				return (0.15*0.8)
		if(act==5 and m1-m2==0):
			if(p2==4 and (a1-a2==1) and (h2-h1==-25)):
				return (0.5*0.8)
			if(p2==4 and (a1-a2==1) and (h2-h1==0)):
				return (0.5*0.8)
		if(act==6 and a1-a2==0 and m1-m2==0):
			if(p2==4  and (h2-h1==-50)):
				return (0.1*0.8)
			if(p2==4  and (h2-h1==0)):
				return (0.9*0.8)
		return 0
	if(s1==0 and s2==1):#mm from doramnt to active
		if(act==0 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==1):
				return (0.85*0.2)
			if(p2==2):
				return (0.15*0.2)
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (0.85*0.2)
			if(p2==2):
				return (0.15*0.2)
		if(act==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==3):
				return (0.85*0.2)
			if(p2==2):
				return (0.15*0.2)
		if(act==3 and p2==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			return (1*0.2)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (0.85*0.2)
			if(p2==2):
				return (0.15*0.2)
		if(act==5 and m1-m2==0):
			if(p2==4 and (a1-a2==1) and (h2-h1==-25)):
				return (0.5*0.2)
			if(p2==4 and (a1-a2==1) and (h2-h1==0)):
				return (0.5*0.2)
		if(act==6 and a1-a2==0 and m1-m2==0):
			if(p2==4  and (h2-h1==-50)):
				return (0.1*0.2)
			if(p2==4  and (h2-h1==0)):
				return (0.9*0.2)
		return 0
	if(s1==1 and (s2==1)):#mm from active to active
		if(act==0 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==1):
				return (0.85*0.5)
			if(p2==2):
				return (0.15*0.5)
		if(act==1 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==0):
				return (0.85*0.5)
			if(p2==2):
				return (0.15*0.5)
		if(act==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==3):
				return (0.85*0.5)
			if(p2==2):
				return (0.15*0.5)
		if(act==3 and p2==2 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			return (1*0.5)
		if(act==4 and a1-a2==0 and m1-m2==0 and h1-h2==0):
			if(p2==4):
				return (0.85*0.5)
			if(p2==2):
				return (0.15*0.5)
		if(act==5 and m1-m2==0):
			if(p2==4 and (a1-a2==1) and (h2-h1==-25)):
				return (0.5*0.5)
			if(p2==4 and (a1-a2==1) and (h2-h1==0)):
				return (0.5*0.5)
		if(act==6 and a1-a2==0 and m1-m2==0):
			if(p2==4  and (h2-h1==-50)):
				return (0.1*0.5)
			if(p2==4  and (h2-h1==0)):
				return (0.9*0.5)
		return 0
	if(s1==1 and (s2==0)):#mm from active to dormant
		if(a2==0 and h2-h1==25):
			if(act==0 and  m1-m2==0):
				if(p2==4):
					reward=reward-40
					return (1*0.5)
			if(act==1  and m1-m2==0):
				if(p2==4):
					reward=reward-40
					return (1*0.5)
			if(act==2 and m1-m2==0):
				if(p2==4):
					reward=reward-40
					return (1*0.5)
			if(act==3 and m1-m2==0):
				if(p2==4):
					reward=reward-40
					return (1*0.5)
			if(act==4 and m1-m2==0):
				if(p2==4):
					reward=reward-40
					return (1*0.5)
			if(act==5 and m1-m2==0):
				if(p2==4):
					reward=reward-40
					return (1*0.5)
			if(act==6 and m1-m2==0):
				if(p2==4):
					reward=reward-40
					return (1*0.5)
			return 0

		return 0
	return 0


def map_pos(p1):
	if p1==4:
		return "C"
	if p1==2:
		return "E"
	if p1==0:
		return "W"	
	if p1==1:
		return  "N"
	if p1==3:
		return "S"	
def State_mm(s1):
	if s1==1:
		return "R"
	if s1==0:
		return "D"
def perform(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	if p1==4:
		return(centre(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))
	if p1==2:
		return(east(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))
	if p1==0:
		return(west(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))	
	if p1==1:
		return(north(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))
	if p1==3:
		return(south(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))	
	return 0
def perform1(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2):
	if p1==4:
		return(centre(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))
	if p1==2:
		return(east1(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))
	if p1==0:
		return(west(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))	
	if p1==1:
		return(north(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))
	if p1==3:
		return(south(act,p1,p2,m1,m2,a1,a2,s1,s2,h1,h2))	
	return 0

def start(Start_p,Start_m,Start_a,Start_s,Start_h,gamma,cost,delta,action,cost1,ee):
	
	actions_num=9
	health=5
	arrows=4
	material=3
	state=2
	position=5
	utilities=np.zeros((position,material,arrows,state,health))
	actions=np.zeros((position,material,arrows,state,health))
	delta_copy=1e13
	ietrations=0
	while(delta_copy>delta):
		temp_array=np.zeros((position,material,arrows,state,health))
		temp_array[:]=-10e13
		temp_array[0,:,:,:,:]=0
		delta_copy=-10e13
		
		for p1 in range (0,position):
			for m1 in range (0,material):
				for a1 in range(0,arrows):
					for s1 in range(0,state):
						for h1 in range(0,health):
							for act in range(0,actions_num):
								if act ==9 or (p1==0 and (act==1 or act==0 or act==2 or act==6 or act==7 or act==8 or act==9)) or (p1==1 and (act==1 or act==0 or act==3 or act==6 or act==5 or act==8 or act==9)) or (p1==2 and (act==2 or act==0 or act==3  or act==7 or act==8 or act==9)) or (p1==3 and (act==1 or act==2 or act==3 or act==6 or act==5 or act==7 or act==9)) or (p1==4 and (act==7 or act==8 or act==9))  or (act==7 and (m1<=0)) or (act==5 and (a1<=0 or a1>3)):
									continue
								temp=0
								for p2 in range (0,position):
									for m2 in range (0,material):
										for a2 in range(0,arrows):
											for s2 in range(0,state):
												for h2 in range(0,health):
													global reward
													reward=cost
													if(act==4 and cost1==100):
														rewards=0
													if(h2==0):
														reward+=50
													if(ee==100):
														temp+=(perform1(act,p1,p2,m1,m2,a1,a2,s1,s2,h1*25,h2*25)*(reward+(gamma*utilities[p2,m2,a2,s2,h2])))
													else:
														temp+=(perform(act,p1,p2,m1,m2,a1,a2,s1,s2,h1*25,h2*25)*(reward+(gamma*utilities[p2,m2,a2,s2,h2])))

								temp=round(temp,11)
								#print("("+map_pos(p1)+","+str(m1)+","+str(a1)+","+State_mm(s1)+","+str(h1*25)+"):"+mapact(act)+"=["+str(temp)+"]")
								if(temp_array[p1,m1,a1,s1,h1]==0 or temp_array[p1,m1,a1,s1,h1]==-10e13 or (temp)>=temp_array[p1,m1,a1,s1,h1]):
									temp_array[p1,m1,a1,s1,h1]=temp
							if(abs(temp_array[p1,m1,a1,s1,h1]-utilities[p1,m1,a1,s1,h1])>delta_copy):								
								delta_copy=abs(temp_array[p1,m1,a1,s1,h1]-utilities[p1,m1,a1,s1,h1])
							if(ietrations==action):
								delta_copy=0
							

							#print("Selected ",temp_array[p1,m1,a1,s1,h1])

		np.copyto(utilities, temp_array)
		temp_actions=np.zeros((position,material,arrows,state,health))
		actions[:]=-1000000000000
		temp_actions[:]=-1000000000000
		actions[0,:,:,:,:]=-1
		temp_actions[0,:,:,:,:]=-1
		ietrations+=1
		print("iteration=",ietrations)
		for p1 in range (0,position):
			for m1 in range (0,material):
				for a1 in range(0,arrows):
					for s1 in range(0,state):
						for h1 in range(0,health):
							for act in range(0,actions_num):
								if act==9 or (p1==0 and (act==1 or act==0 or act==2 or act==6 or act==7 or act==8 or act==9)) or (p1==1 and (act==1 or act==0 or act==3 or act==6 or act==5 or act==8 or act==9)) or (p1==2 and (act==2 or act==0 or act==3  or act==7 or act==8 or act==9)) or (p1==3 and (act==1 or act==2 or act==3 or act==6 or act==5 or act==7 or act==9)) or (p1==4 and (act==7 or act==8 or act==9))  or (act==7 and (m1<=0)) or (act==5 and (a1<=0 or a1>3)) or (act==8 and (m1<=0)):
									continue
								temp=0
								for p2 in range (0,position):
									for m2 in range (0,material):
										for a2 in range(0,arrows):
											for s2 in range(0,state):
												for h2 in range(0,health):
													reward=cost
													if(act==4):
														rewards=0
													if(h2==0):
														reward+=50
													if(ee==100):
														temp+=(perform1(act,p1,p2,m1,m2,a1,a2,s1,s2,h1*25,h2*25)*(reward+(gamma*utilities[p2,m2,a2,s2,h2])))
													else:
														temp+=(perform(act,p1,p2,m1,m2,a1,a2,s1,s2,h1*25,h2*25)*(reward+(gamma*utilities[p2,m2,a2,s2,h2])))


								#print("("+map_pos(p1)+","+str(m1)+","+str(a1)+","+State_mm(s1)+","+str(h1*25)+"):"+mapact(act)+"=["+str(temp)+"]")
								if((temp)>=temp_actions[p1,m1,a1,s1,h1]):
									actions[p1,m1,a1,s1,h1]=act
									temp_actions[p1,m1,a1,s1,h1]=temp
								if(actions[p1,m1,a1,s1,h1]==-1000000000000 or actions[p1,m1,a1,s1,h1]==-1):
									actions[p1,m1,a1,s1,h1]=act
								#print(temp,temp_actions[p1,m1,a1,s1,h1])

							utilities=np.around(utilities,3)
							if(h1==0):
								actions[p1,m1,a1,s1,h1]=9
								utilities[p1,m1,a1,s1,h1]=0
							print("("+map_pos(p1)+","+str(m1)+","+str(a1)+","+State_mm(s1)+","+str(h1*25)+"):"+mapact(actions[p1,m1,a1,s1,h1])+"=["+str(utilities[p1,m1,a1,s1,h1])+"]")

original = sys.stdout
os.mkdir("./outputs")
											
def main():	
	Start_p=0
	Start_m=0
	Start_h=0
	Start_a=0
	Start_s=0
	delta=10e-3
	gamma=0.999
	cost=-5		
	action=16
	cost1=0			
	start(Start_p,Start_m,Start_a,Start_s,Start_h,gamma,cost,delta,action,cost1,0)
#check for rewards

sys.stdout = open('./outputs/part_2_trace.txt', 'w')
main()
sys.stdout = original

def main1():	
	Start_p=0
	Start_m=0
	Start_h=0
	Start_a=0
	Start_s=0
	delta=10e-3
	gamma=0.25
	cost=-5
	action=15	
	cost1=0				
	start(Start_p,Start_m,Start_a,Start_s,Start_h,gamma,cost,delta,15,cost1,0)

sys.stdout = open('./outputs/part_2_task_2.3_trace.txt', 'w')
main1()
sys.stdout = original

def main2():	
	Start_p=0
	Start_m=0
	Start_h=0
	Start_a=0
	Start_s=0
	delta=10e-3
	gamma=0.999
	cost=-5
	action=50
	cost1=100					
	start(Start_p,Start_m,Start_a,Start_s,Start_h,gamma,cost,delta,action,cost1,0)

sys.stdout = open('./outputs/part_2_task_2.2_trace.txt', 'w')
main2()
sys.stdout = original

def main3():	
	Start_p=0
	Start_m=0
	Start_h=0
	Start_a=0
	Start_s=0
	delta=10e-3
	gamma=0.999
	cost=-5
	action=19
	cost1=100					
	start(Start_p,Start_m,Start_a,Start_s,Start_h,gamma,cost,delta,action,cost1,100)

sys.stdout = open('./outputs/part_2_task_2.1_trace.txt', 'w')
main3()
sys.stdout = original




