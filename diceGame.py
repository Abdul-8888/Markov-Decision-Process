import random
class DiceMDP:
    def states(self):
        return ['in', 'end']
    
    def startState(self):
        return 'in'
    
    def isGoal(self,s):
        if s == 'end':
            return True
        else:
            return False
        
    def actions(self,s):
        if s == 'in':
            return ['stay', 'quit']
        elif s == 'end':
            return []
        
    def transitionProbabilities(self,s,a,p):
        if s=='in' and a=='quit' and p=='end':
            return 1
        elif s=='in' and a=='stay' and p=='in':
            return 2/3
        elif s=='in' and a=='stay' and p=='end':
            return 1/3
        else:
            return 0

    def takeAction(self,s,a):
        if s == 'in' and a == 'quit':
            return 'end'
        
        if s=='in' and a=='stay':
            d = random.randint(1,6)
            # print('dice rolled: ' , d)

            if d == 1 or d == 2:
                return 'end'
            else:
                return 'in'
            
    def reward(self,a):
        if a == 'stay':
            return 4
        else:
            return 10
        

def policyEvaluation(mdp: DiceMDP, policy):
    v = {}
    p_v = {}

    states = mdp.states()

    for i in states:
        v[i] = 0
        p_v[i] = 0

    for i in range(1,100):
        for s in states:
            c = 0.0
            for n in states:
                c += mdp.transitionProbabilities(s,policy,n) * (mdp.reward(policy) + (1*(p_v[n])))
            
            v[s] = c
            p_v = v

        # diff = []
        # for i in range(0,len(v)):
        #     diff.append(abs(v[i] + p_v[i]))
        #     if (max(diff) <= 2):
        #         break

    print(v)
    return v

def policyValue(mdp:DiceMDP):
    maximum = {}
    for policy in mdp.actions('in'):
        maximum[policy] = policyEvaluation(mdp, policy)
        
    return max(maximum)

def main():
    model = DiceMDP()
    rewards = []

    for i in range(0,100):
        # print('outer-loop: ', i)
        current = model.startState()
        total_reward = 0

        while not model.isGoal(current):
            # print('inner-loop')
            a = 'stay'

            current = model.takeAction(current, a)
            total_reward += model.reward(a)

        # print('Ended game ', i)
        rewards.append(total_reward)

    # print(rewards)

    dict = {}
    for i in rewards:
        if i not in dict:
            dict[i] = 1
        else:
            dict[i] += 1

    # print(dict)
    print(policyValue(model))

if __name__ == '__main__':
    main()