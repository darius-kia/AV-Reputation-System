import random
import matplotlib.pyplot as plt
import matplotlib
import time
import numpy as np

OPPOSITE = {1: 0, 0: 1}

class AV:
    def __init__(self, model, vID, status):
        self.model = model
        self.vID = vID
        self.status = status
        #status: 0 = malicious, 1 = not malicious

    def __repr__(self):
        return self.vID + f"({self.status})"

    def broadcast(self, recipients):
        witnesses = random.sample(recipients, int(len(recipients)*random.random()*0.5)) # picks n number of witnesses where n is between 0 and 50% of the recipients
        r = random.choice(self.model.RSUs) # pick a random RSU
        transaction = {} # key is witness, value is witness's score
        expectedValue = self.status # change later once more statuses
        for w in witnesses:
           transaction[w] = w.score(self, expectedValue) # have each witness score the transaction
        r.updateOperatingRep(self, transaction, 0.05)

    def score(self, sender, expected):
        #score must take into account the status of the AV that is witnessing the transaction
        # score = random.choice([0, 1]) # make it depend on status
        
        return expected if self.status == 1 else OPPOSITE[expected]
        # add nuance; good vehicles sometimes give bad scores

class RSU:

    def __init__(self, model, rID):
        self.model = model
        self.rID = rID
        self.reputation_scores = {} # key is the av, value is its current reputation; should be stored by BS, RSU stores transaction info
    
    def __repr__(self):
        return self.rID

    def updateOperatingRep(self, sender, transaction, velocity):
        # update the reputation of sender AV using the transaction
        # does this by iterating through the witness scores for the transaction and get weighted average
        tRep = 0
        repSum = sum([self.reputation_scores[w] for w in transaction.keys()])
        for w in transaction.keys():
            weight = self.reputation_scores[w] / repSum
            tRep += transaction[w] * weight

        currRep = self.reputation_scores[sender]
        self.reputation_scores[sender] = tRep * velocity + currRep * (1-velocity) # maybe change: first few transactions shouldn't have 95% weight; maybe have the 95 start off low and get higher over time
        # update reputation for every RSU
        # TO-DO weight based on recency AND number of witnesses
        

    def updateReportingRep(self):
        pass

class Model:
    def __init__(self, nAVs, nRSUs, propNormal):
        # 270 status 0, 15 status 1, 10 status 2, 5 status 3
        # Decide how many AVs of each type (not random -> could use proportions later on in the simulation)
        # 90% good vehicles and 10% malicous vehicles
        statuses = [1]*int(round(nAVs*propNormal)) + [0]*(int(round(nAVs*(1-propNormal))))
        self.AVs = [AV(self, f"AV_{i}", statuses[i]) for i in range(nAVs)]
        self.RSUs = [RSU(self, f"RSU_{i}") for i in range(nRSUs)]
        # self.current_tick = 0
    
    def initialize_reputations(self):
        reps = {av: 1.0 for av in self.AVs} # give each av a default of 1.0
        for r in self.RSUs:
            r.reputation_scores = reps # set the default reps for each rsu
    
    def step(self):
        # tick = self.current_tick % 1440 # get tick of current day
        # if tick is 0:
        #     # end of day
        pass
        
    def plot(self):
        scores = self.RSUs[0].reputation_scores
        x1 = [str(i) for i in scores.keys()]
        y1 = list(scores.values()) 
        plt.bar(x1, y1)
        plt.show()


    def run(self, n_transactions):
        self.initialize_reputations()
        for i in range(n_transactions):
            av = random.choice(self.AVs)
            nRecipients = int(random.random()*10+10)
            recipients = random.sample([v for v in self.AVs if v is not av], nRecipients) # pick recipients as long as they aren't the sender
            av.broadcast(recipients)
        # for (int i = 0; i < n_days; i++){ broadcast ()}

model = Model(30, 1, 0.9) # start off with 1 rsu
model.run(2000)
scores = model.RSUs[0].reputation_scores
print(scores)
model.plot()