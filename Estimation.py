import copy

class reward:
    def __init__(self, cs, a, ns, r):
        self.currentState = cs
        self.action = a
        self.nextState = ns
        self.amount = r

class MDP:

    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.isGoal = []
        # self.successStates = []
        # self.failureStates = []
        self.episodes = []

    def addState(self, s):
        if s not in self.states:
            self.states.append(s)

    def getStates(self):
        return self.states
    
    def addAction(self, a):
        if a not in self.actions:
            self.actions.append(a)

    def getActions(self):
        return self.actions
    
    def addReward(self, r):
        self.rewards.append(r)

    def getRewards(self):
        return self.rewards
    
    # def isGoal(self, s):
    #     return True if s in self.successStates or s in self.failureStates else False
    
    def discount(self):
        return 1
    
    def reward(self,s,a,n):
        for rew in self.rewards:
            if rew.currentState == s and rew.action == a and rew.nextState == n:
                return rew.amount
        return 0
    
    def transitionProbabilities(self,s,a,n):
        denominator = 0
        numerator = 0
        
        for rew in self.rewards:
            if s == rew.currentState and a == rew.action:
                denominator += 1
                if n == rew.nextState:
                    numerator += 1

        if denominator != 0:
            return numerator/denominator
        
        return 0



######################################################################################################## Functions
def valueIteration(model: MDP, current, policy):
    v = {}
    p_v = {}

    states = model.getStates()

    v[current] = 0
    p_v[current] = 0

    for i in range(1,100):
        c = 0.0
        for n in states:
            c += model.transitionProbabilities(current,policy,n) * (model.reward(current,policy,n) + (model.discount()*(p_v[current])))
            
        v[current] = c
        p_v = copy.deepcopy(v)

    print(v)
    return v

def policyIteration(mdp: MDP):
    actions = {}

    for state in mdp.getStates():

        if state in mdp.isGoal:
            actions[state] = "None"
            continue

        max = float('-inf')
        action = None

        for a in mdp.getActions():
            value = valueIteration(mdp, state, a)[state]
            if value > max:
                max = value
                action = a
            # elif value == max:
            #     print(action, a)

        actions[state] = action
    
    return actions

def fileHandling(path):
    model = MDP()
    prevEpisode = 1
    idx = 0
    # prevReward = 0
    # prevNext = 0
    try:
        with open(path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')

                if len(parts) == 5:
                    episode = int(parts[0])
                    currentState = int(parts[1])
                    action = parts[2]
                    nextState = int(parts[3])
                    rew = int(parts[4])

                    model.addState(currentState)
                    model.addAction(action)
                    model.addState(nextState)
                    r = reward(currentState, action, nextState, rew)
                    model.addReward(r)

                    if episode != prevEpisode:
                        model.episodes.append(idx)
                        # if rew > prevReward and prevNext not in model.successStates:
                    #         model.successStates.append(prevNext)
                    #     elif prevReward > rew and prevNext not in model.failureStates:
                    #         model.failureStates.append(prevNext)

                    # print(f"Episode: {episode}, Current State: {currentState}, Action: {action}, Next State: {nextState}, Reward: {rew}")
                    prevEpisode = episode
                    # prevReward = rew
                    idx += 1
                else:
                    print(f"error reading line {len(parts)}")

    except Exception as e:
        print("Error: ", e)
    
    return model

def settingMDP(model: MDP):
    for i in model.episodes:
        # if model.rewards[i-1].amount >= model.rewards[i-2].amount and model.rewards[i-1].nextState not in model.isGoal:
        model.isGoal.append(model.rewards[i-1].nextState)
        # elif model.rewards[i-1].amount < model.rewards[i-2].amount and (model.rewards[i-1].nextState not in model.successStates and model.rewards[i-1].nextState not in model.failureStates):
        #     model.failureStates.append(model.rewards[i-1].nextState)
        # else:
        #     print(model.rewards[i-1].nextState)

    arr = copy.deepcopy(model.rewards)
    for i in range(1, len(model.rewards)):
        model.rewards[i].amount -= arr[i-1].amount
    #     print(model.rewards[i].amount)
    # print(model.rewards[0].amount)

    return model

######################################################################################################## Main
def main():
    path = 'D:\Study\AI\Markov Desicion Process\AI_TEST.txt'
    model = fileHandling(path)
    model = settingMDP(model)

    for r in model.rewards:
        print(r.currentState, r.action, r.nextState, r.amount)

    result = policyIteration(model)
    print(result)

if __name__ == "__main__":
    main()
