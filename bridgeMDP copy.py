import math


class bridgeMDP:

    def __init__(self, r, c):
        self.nr = r
        self.nc = c

    def states(self):
        return list(range(1, self.nr*self.nc+1))

    def startState(self, x, y):
        self.startState = self.getStateNo(y, x)

    def getBlockNo(self, s):
        x = (s % self.nc)
        y = math.ceil(s/self.nc)
        if (x == 0):
            x = self.nc
        return (x, y)

    def getStateNo(self, x, y):
        return (x-1)*self.nc + y

    def actions(self, s):
        list = []
        x, y = self.getBlockNo(s)

        if (y-1 >= 1):
            list.append('up')
        if (y+1 <= self.nr):
            list.append('down')
        if (x-1 >= 1):
            list.append('left')
        if (x+1 <= self.nc):
            list.append('right')

        return list

    def failureStates(self):
        return [3, 7]

    def successStates(self):
        return [4]

    def isGoal(self, s):
        if s in self.failureStates() or s in self.successStates():
            return True
        else:
            return False

    def discount(self):
        return 1

    def reward(self, s, a, n):

        x, y = self.getBlockNo(s)

        # if n in self.failureStates():
        #     return -50
        # elif n in self.successStates():
        #     return 20
        # elif n == 9:
        #     return 2
        # else:
        #     return 0
        if a == 'up':
            if (y-1 >= 1):  # up
                up = self.getStateNo(y-1, x)
                if up == n:
                    if n in self.failureStates():
                        return -50
                    elif n in self.successStates():
                        return 20
                    elif n == 9:
                        return 2
                    else:
                        return 1

        elif a == 'down':
            if (y+1 <= self.nr):  # down
                down = self.getStateNo(y+1, x)
                if down == n:
                    if n in self.failureStates():
                        return -50
                    elif n in self.successStates():
                        return 20
                    elif n == 9:
                        return 2
                    else:
                        return 1

        elif a == 'left':
            if (x-1 >= 1):  # left
                left = self.getStateNo(y, x-1)
                if left == n:
                    if n in self.failureStates():
                        return -50
                    elif n in self.successStates():
                        return 20
                    elif n == 9:
                        return 2
                    else:
                        return 1

        elif a == 'right':
            if (x+1 <= self.nc):  # right
                right = self.getStateNo(y, x+1)
                if right == n:
                    if n in self.failureStates():
                        return -50
                    elif n in self.successStates():
                        return 20
                    elif n == 9:
                        return 2
                    else:
                        return 1
        return 0

    def transitionProbabilities(self, s, a, n):

        if self.isGoal(s):
            return 0

        x, y = self.getBlockNo(s)
        up = None
        down = None
        left = None
        right = None

        if (x-1 >= 1):  # left
            left = self.getStateNo(y, x-1)
        if (y-1 >= 1):  # up
            up = self.getStateNo(y-1, x)
        if (x+1 <= self.nc):  # right
            right = self.getStateNo(y, x+1)
        if (y+1 <= self.nr):  # down
            down = self.getStateNo(y+1, x)

        if up not in self.failureStates() and down not in self.failureStates() and left not in self.failureStates() and right not in self.failureStates():
            if a == 'up' and n == up:
                return 1
            elif a == 'down' and n == down:
                return 1
            elif a == 'left' and n == left:
                return 1
            elif a == 'right' and n == right:
                return 1
            return 0

        else:
            if a == 'up' and n == up:
                return 0.6
            elif a == 'down' and n == down:
                return 0.6
            elif a == 'left' and n == left:
                return 0.6
            elif a == 'right' and n == right:
                return 0.6
            else:
                if n in self.failureStates():
                    return 0.4
                else:
                    return 0

    def takeAction(self, s, a):
        x, y = self.getBlockNo(s)

        if a == 'up':
            return self.getStateNo(y-1, x)
        elif a == 'down':
            return self.getStateNo(y+1, x)
        elif a == 'left':
            return self.getStateNo(y, x-1)
        elif a == 'right':
            return self.getStateNo(y, x+1)
        else:
            return None


def policyEvaluation(mdp: bridgeMDP, policy):
    v = {}
    p_v = {}

    states = mdp.states()

    for i in states:
        v[i] = 0
        p_v[i] = 0

    for i in range(1, 100):
        for s in states:
            c = 0.0
            for n in states:
                c += mdp.transitionProbabilities(s, policy, n) * (
                    mdp.reward(s, policy, n) + (mdp.discount()*(p_v[n])))

            p_v = v
            v[s] = c

    return v


def policyValue(mdp: bridgeMDP):
    maximum = {}
    for policy in mdp.actions(6):
        maximum[policy] = policyEvaluation(mdp, policy)

    actions = {}
    for i in range(1, 13):
        actions[i] = []
        actions[i].append(maximum['up'][i])
        actions[i].append(maximum['down'][i])
        actions[i].append(maximum['left'][i])
        actions[i].append(maximum['right'][i])

    optimalActions = {}
    maxIdx = []
    for k, v in actions.items():
        maxValue = max(v)
        maxIdx = v.index(maxValue)

        a = ''
        if maxIdx == 0:
            a = 'up'
        elif maxIdx == 1:
            a = 'down'
        if maxIdx == 2:
            a = 'left'
        if maxIdx == 3:
            a = 'right'
        if k in mdp.failureStates() or k in mdp.successStates():
            a = 'none'
        optimalActions[k] = (a, maxValue)

    return optimalActions


def main():
    model = bridgeMDP(3, 4)

    actions = policyValue(model)

    for k, v in actions.items():
        print(f'state {k}: {v}')


if __name__ == "__main__":
    main()
