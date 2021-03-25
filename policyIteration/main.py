def improvePolicy(state):
  return rewards[state] + gamma * values[state]

import random
random.seed();

states = {
    'A': {1: 'B', 2: 'C'},
    'B': {1: 'D', 2: 'A'},
    'C': {1: 'A', 2: 'D'},
}

values = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 100,
}

rewards = {
    'A': -10,
    'B': -10,
    'C': -10,
    'D': 100,
}

policy = {
    1: {'A': {1: 1, 0: 0}, 'B': {1: 1, 0: 0}, 'C': {1: 1, 0: 0}, 'D': {1: 1, 0: 0}},

}

def getAction(state, policyNum): 
    prob = random.random()
    action = random.random()
    if action <= policy[policyNum][state][1]:
        action = 1
    else:
        action = 2

    if prob >= 0.9:
        return action
    else:
        return 2 if action == 1 else 1

def V(state, policy):
    if (state == 'D'):
        return values['D']

    newVal = V(states[state][getAction(state, policy)], policy)

    values[state] = (values[state] +  rewards[state] + gamma * newVal) / 2
    return values[state]

def resetValues():
    values = {
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 100,
    }

    return values

gamma = 1
print("Policy 1: ")
values = resetValues()
diff = 100

print("Starting Policies:")
print("1: ", policy[1])

last = {'A': 1, 'B': 1, 'C': 1, 'D': 1}
flag = True
while flag:
    V('A', 1)
    for p in policy[1]:
        if (p == 'D'):
            break
        policy[1][p][1] = improvePolicy(p) / 100
        policy[1][p][0] = 1 - policy[1][p][1]
        
        if abs(last[p] - policy[1][p][1]) == 0:
            flag = False
        last[p] = policy[1][p][1]


print("\nEnd Policies:")
print("1: ", policy[1])
# print(values)
