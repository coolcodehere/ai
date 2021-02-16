# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 17:13:01 2017

@author: xfang13
"""

import numpy as np
import copy


def action(state):
    x,y = np.where(state == 0)
    x = x[0]
    y = y[0]
    result = []
    if x + 1 <= 1:
        state_copy = copy.deepcopy(state)
        temp = state_copy[x][y]
        state_copy[x][y] = state_copy[x+1][y]
        state_copy[x+1][y] = temp
        result.append(state_copy)
    if x - 1 >= 0:
        state_copy = copy.deepcopy(state)
        temp = state_copy[x][y]
        state_copy[x][y] = state_copy[x-1][y]
        state_copy[x-1][y] = temp
        result.append(state_copy)
    if y + 1 <= 1:
        state_copy = copy.deepcopy(state)
        temp = state_copy[x][y]
        state_copy[x][y] = state_copy[x][y+1]
        state_copy[x][y+1] = temp
        result.append(state_copy)
    if y - 1 >= 0:
        state_copy = copy.deepcopy(state)
        temp = state_copy[x][y]
        state_copy[x][y] = state_copy[x][y-1]
        state_copy[x][y-1] = temp
        result.append(state_copy)
        
    return result

# Descriptions:
# search_history is a list
# explored is a list
# action() is a function that generates a list of possible results

def solvable(goal):
	search_history = goal
	explored = goal
	possible_moves = action(goal)
	flag1 = True
	search_history.append(possible_moves)
	explored.concatenation(possible_moves)
	while flag1:
		new_states = []
		for state, i, in search_history[len(search_history) - 1]:
			for state, j, in action(i):
				flag2 = False
				for state, k, in explored:
					if np.array_equals(j,k):
						flag2 = True
						break
				if flag2 is False:
					explored.append(j)
					new_states.append(j)
		if not new_states:
			print('Search complete')
			flag1 = False
		else:
			search_history.append(new_states)
	return explored
  
if __name__ == '__main__':
    results = action(np.asarray([[1,0],[3,2]])) 
    print (results)               