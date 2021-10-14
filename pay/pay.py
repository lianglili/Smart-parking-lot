import os 
import numpy  as np
import math

def pay(ap,time):
	cur_dir = os.getcwd().replace('\\','/')
	path = os.path.join(cur_dir, 'Txtnetdata/pay.txt')
	stand = np.loadtxt(path)
	if ap:
		if time < stand[0]:
			return 0	
		else:
			return stand[2]*(math.ceil(time-stand[0]))
	else:
		if time < stand[0]:
			return 0
		else:
			return stand[1]*(math.ceil(time-stand[0]))
