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
        witnesses = random.sample(recipients, int(len(recipients)*random.random()*0.5+1)) # picks n number of witnesses where n is between 0 and 50% of the recipients
        r = random.choice(self.model.RSUs) # pick a random RSU
        transaction = {} # key is witness, value is witness's score
        expectedValue = self.status # change later once more statuses // add noise
        for w in witnesses:
           transaction[w] = w.score(self, expectedValue, 0.95) # have each witness score the transaction
        r.addTransaction(transaction)
        r.updateOperatingRep(self, transaction, 0.05, True, True)
        for w in witnesses:
           r.updateReportingRep(w, transaction, 0.05, weightWitnessRep=True) # update the reputation of each witness

    def score(self, sender, expected, noise):
        #score must take into account the status of the AV that is witnessing the transaction
        # score = random.choice([0, 1]) # make it depend on status
        # if a vehicle that is scoring a transaction has its reputation fall below 0.4 disregards the scoring from the vehicle
        if self.status == 1:
            if random.random() < noise:
                return expected 
            else:
                return OPPOSITE[expected]
        elif self.status == 0:
            if random.random() < noise:
                return OPPOSITE[expected]
            else:
                return expected

        # add nuance; good vehicles sometimes give bad scores

class RSU:

    def __init__(self, model, rID):
        self.model = model
        self.rID = rID
        self.operating_scores = {} # key is the av, value is its current reputation; should be stored by BS, RSU stores transaction info
        self.reporting_scores = {}
        self.transactions = []
        self.avgWitnesses = 0
    
    def __repr__(self):
        return self.rID

    def addTransaction(self, newT): 
        # update avg witnesses
        self.avgWitnesses = ((self.avgWitnesses * len(self.transactions)) + len(newT)) / (len(self.transactions) + 1)
        # note: does not update prior transactions
        self.transactions.append(newT)

    def updateOperatingRep(self, sender, transaction, velocity, weightWitnessRep=True, weightNumWitnesses=True):
        # update the reputation of sender AV using the transaction
        # does this by iterating through the witness scores for the transaction and get weighted average
        oRep = 0
        repSum = sum([self.reporting_scores[w] for w in transaction.keys()])
        if weightWitnessRep:
            for w in transaction.keys():
                weight = self.reporting_scores[w] / repSum
                oRep += transaction[w] * weight
        else: # not weighting by witness reputations
            oRep = sum([transaction[w] for w in transaction.keys()])/len(transaction.keys())

        if weightNumWitnesses:
            k = 2
            diff = len(transaction) - self.avgWitnesses
            shift = diff / k
            velocity += (shift*0.01)

        currRep = self.operating_scores[sender]
        
        self.operating_scores[sender] = oRep * velocity + currRep * (1-velocity) # maybe change: first few transactions shouldn't have 95% weight; maybe have the 95 start off low and get higher over time
        # update reputation for every RSU
        # TO-DO weight based on recency AND number of witnesses
        

    def updateReportingRep(self, witness, transaction, velocity, weightWitnessRep=True):
        # Calculate the average score based on the same method as used in Operating Reputation
        # 0.2 rep vehicle (malicious) reports 0 on a good transaction and 0.9 rep vehicle (non-malicious) reports 1 on a good transaction
        rRep = 0
        if weightWitnessRep:
            repSum = sum([self.reporting_scores[w] for w in transaction.keys()])
            for w in transaction.keys():
                weight = self.reporting_scores[w] / repSum
                rRep += transaction[w] * weight
        else: # not weighting by witness reputations
            rRep = sum([transaction[w] for w in transaction.keys()])/len(transaction.keys())
        deviation = 1 - abs(transaction[witness] - rRep)
        currRep = self.reporting_scores[witness]
        self.reporting_scores[witness] = deviation * velocity + currRep * (1-velocity)


class Model:
    def __init__(self, nAVs, nRSUs, propNormal):
        # 270 status 0, 15 status 1, 10 status 2, 5 status 3
        # Decide how many AVs of each type (not random -> could use proportions later on in the simulation)
        # 90% good vehicles and 10% malicous vehicles
        numN = int(round(nAVs*propNormal))
        numM = int(round(nAVs*(1-propNormal)))
        statuses = [1]*numN + [0]*numM
        self.AVs = [AV(self, f"AV_{i}", statuses[i]) for i in range(nAVs)]
        self.nAVs = self.AVs[:numN] # normal AVs
        self.mAVs = self.AVs[numN:] # malicious AVs

        self.RSUs = [RSU(self, f"RSU_{i}") for i in range(nRSUs)]
        # self.current_tick = 0
    
    def initialize_reputations(self):
        for r in self.RSUs:
            r.operating_scores = {av: 1.0 for av in self.AVs} # give each av a default of 1.0
            r.reporting_scores = {av: 1.0 for av in self.AVs} # give each av a default of 1.0
    
    def step(self):
        # tick = self.current_tick % 1440 # get tick of current day
        # if tick is 0:
        #     # end of day
        pass
        
    def plotOperating(self):
        scores = self.RSUs[0].operating_scores
        x1 = [str(i) for i in scores.keys()]
        y1 = list(scores.values()) 
        plt.xticks(rotation=90)
        plt.bar(x1, y1)
        plt.show()

    def plotReporting(self):
        scores = self.RSUs[0].reporting_scores
        x1 = [str(i) for i in scores.keys()]
        y1 = list(scores.values()) 
        plt.xticks(rotation=90)
        plt.bar(x1, y1)
        plt.show()    


    def calculateOperatingError(self):
        err = 0
        op_scores = self.RSUs[0].operating_scores
        for av in op_scores:
            err += abs(av.status - op_scores[av])
        return err / len(op_scores)

    def calculateReportingError(self):
        err = 0
        re_scores = self.RSUs[0].reporting_scores
        for av in re_scores:
            err += abs(av.status - re_scores[av])
        return err / len(re_scores)

    def turn(self):
        prob = random.random()
        if prob < 0.9:
            if prob > 0.8:
                av = random.choice(self.mAVs) # pick a malicious AV
            else:
                av = random.choice(self.nAVs) # pick a normal AV
            nRecipients = int(random.random()*10+10)
            recipients = random.sample([v for v in self.AVs if v is not av], nRecipients) # pick recipients as long as they aren't the sender
            av.broadcast(recipients)

    def run(self, n_turns, print_error=True):
        self.initialize_reputations()
        for i in range(n_turns):
            self.turn()
        # for (int i = 0; i < n_days; i++){ broadcast ()}
        if print_error:
            print(f"Operating Error: {self.calculateOperatingError()}")
            print(f"Reporting Error: {self.calculateReportingError()}")

model = Model(30, 1, 0.9) # start off with 1 rsu
model.run(2000)
scores = model.RSUs[0].operating_scores
# model.plotOperating()