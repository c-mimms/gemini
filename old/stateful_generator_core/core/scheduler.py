import random

class Scheduler:
    def __init__(self, weights, seed=None):
        self.weights = weights
        self.random = random.Random(seed)

    def pick(self):
        total = sum(self.weights.values())
        r = self.random.uniform(0, total)
        upto = 0
        for key, weight in self.weights.items():
            upto += weight
            if upto >= r:
                return key
        return next(iter(self.weights))
