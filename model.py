import random
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
import os

OPPOSITE = {1: 0, 0: 1}
STATUSES = {0: 'MAL', 1: 'NORM', 2: 'MAL_OP', 3: 'MAL_REP'}


class Params:
    def __init__(self, velocity=0.05, byWitnessRep=False, byNumWitnesses=False, kNumWitnesses=2, useQuartiles=False, numVehicles=100, minRecipients=5, maxRecipients=30, propWitnesses=0.5, propNormal=0.9, broadcastNoise=0.05, witnessNoise=0.05, useMalOp=False, useMalRep=False, numTurns=5000, percTransaction=0.9, percMalicious=0.1):
        # system parameters
        self.velocity = velocity
        self.byWitnessRep = byWitnessRep
        self.byNumWitnesses = byNumWitnesses
        self.kNumWitnesses = kNumWitnesses
        self.useQuartiles = useQuartiles

        # environment parameters
        self.numVehicles = numVehicles
        self.minRecipients = minRecipients
        self.maxRecipients = maxRecipients
        self.propWitnesses = propWitnesses
        self.propNormal = propNormal
        self.broadcastNoise = broadcastNoise
        self.witnessNoise = witnessNoise
        self.useMalOp = useMalOp
        self.useMalRep = useMalRep
        self.numTurns = numTurns
        self.percTransaction = percTransaction
        self.percMalicious = percMalicious
    def __repr__(self):
        return f"{self.velocity},{self.byWitnessRep},{self.byNumWitnesses},{self.kNumWitnesses},{self.useQuartiles},{self.numVehicles},{self.minRecipients},{self.maxRecipients},{self.propWitnesses},{self.propNormal},{self.broadcastNoise},{self.witnessNoise},{self.useMalOp},{self.useMalRep},{self.numTurns},{self.percTransaction},percMalicious"
        
args = sys.argv[1:]
assert(len(args) == 16 or len(args) == 0), "Must include all arguments"
PARAMS = Params(*args)


class AV:
    def __init__(self, model, vID, status):
        self.model = model
        self.vID = vID
        self.status = status

    def __repr__(self):
        return self.vID + f"({STATUSES[self.status]})"

    def broadcast(self, recipients):
        witnesses = random.sample(recipients, int(len(recipients)*random.random()*PARAMS.propWitnesses+1)) # picks n number of witnesses where n is between 0 and k% of the recipients
        r = random.choice(self.model.RSUs) # pick a random RSU
        transaction = {} # key is witness, value is witness's score

        expectedValue = 1 if self.status in [1, 3] else 0
        if random.random() < PARAMS.broadcastNoise:
            expectedValue = OPPOSITE[expectedValue]
        for w in witnesses:
           transaction[w] = w.score(self, expectedValue) # have each witness score the transaction
        r.addTransaction(transaction)
        r.updateOperatingRep(self, transaction)
        for w in witnesses:
           r.updateReportingRep(w, transaction) # update the reputation of each witness

    def score(self, sender, expected):
        #score must take into account the status of the AV that is witnessing the transaction
        # score = random.choice([0, 1]) # make it depend on status
        # if a vehicle that is scoring a transaction has its reputation fall below 0.4 disregards the scoring from the vehicle
        scores = [0, 0.25, 0.5, 0.75, 1.0]
        wScore = -99
        if PARAMS.useQuartiles:
            wScore = expected if self.status in [1, 2] else OPPOSITE[expected] # if the vehicle is normal or malicious operating, rate accurately
            if random.random() < PARAMS.witnessNoise:
                wScore = random.choice([i for i in scores if i != wScore]) # if there's noise, randomly pick a different score
        else: # use binary scores
            wScore = expected if self.status in [1, 2] else OPPOSITE[expected]
            if random.random() < PARAMS.witnessNoise:
                wScore = OPPOSITE[wScore] # if there's noise, flip the score
        return wScore

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
        self.avgWitnesses = ((self.avgWitnesses * len(self.transactions)) + len(newT)) / (len(self.transactions) + 1) # recompute average number of witnesses per transaction
        # note: does not update prior transactions
        self.transactions.append(newT)

    def updateOperatingRep(self, sender, transaction):
        # update the reputation of sender AV using the transaction
        # does this by iterating through the witness scores for the transaction and get weighted average
        oRep = 0
        repSum = sum([self.reporting_scores[w] for w in transaction.keys()]) # get total reputation of every witness
        if PARAMS.byWitnessRep:
            for w in transaction.keys():
                weight = self.reporting_scores[w] / repSum # each vehicle's weight is based on their reputation relative to the sum of all the witnesses' reputations
                oRep += transaction[w] * weight
        else: # not weighting by witness reputations
            oRep = sum([transaction[w] for w in transaction.keys()])/len(transaction.keys()) # simple average

        velocity = PARAMS.velocity
        if PARAMS.byNumWitnesses:
            diff = len(transaction) - self.avgWitnesses
            shift = diff / PARAMS.kNumWitnesses
            velocity += (shift*0.01) # shift the velocity by a value proportional to the difference between the number of witnesses for this transaction and the average across the entire simulation

        currRep = self.operating_scores[sender]
        
        self.operating_scores[sender] = oRep * (velocity) + currRep * (1-velocity) # maybe change: first few transactions shouldn't have 95% weight; maybe have the 95 start off low and get higher over time
        # update reputation for every RSU
        # TO-DO weight based on recency
        

    def updateReportingRep(self, witness, transaction):
        # Calculate the average score based on the same method as used in Operating Reputation
        # 0.2 rep vehicle (malicious) reports 0 on a good transaction and 0.9 rep vehicle (non-malicious) reports 1 on a good transaction
        if PARAMS.useQuartiles:
            # TO-DO: implement weightWitnessRep here
           rRep = sum([transaction[w] for w in transaction.keys()])/len(transaction.keys()) # average rating of the transaction (based on every witness's score)
           snapped = round(rRep*4)/4 # snap the average rating to one of the quartile values
           match = 1 if snapped == transaction[witness] else 0 # if the snapped value is the same as what the witness rated it, then good
           currRep = self.reporting_scores[witness]
           self.reporting_scores[witness] = match * (PARAMS.velocity) + currRep * (1-PARAMS.velocity)
        else:
            rRep = 0
            if PARAMS.byWitnessRep:
                # TO-DO: doesn't feel completely right; why is the weighted average being calculated again when it's already done in updateOperatingRep()?
                #        can be simplified: store the score of the transaction somewhere after updateOperatingRep is called; then access it here without recalculating
                repSum = sum([self.reporting_scores[w] for w in transaction.keys()]) # sum of all the witnesses reputations 
                for w in transaction.keys():
                    weight = self.reporting_scores[w] / repSum # each witnesses weight is based on their reputation relative to the sum
                    rRep += transaction[w] * weight # score of the transaction
            else: # not weighting by witness reputations
                rRep = sum([transaction[w] for w in transaction.keys()])/len(transaction.keys())
            deviation = abs(transaction[witness] - rRep) # deviation is difference between witness's score and average score (subtracted from 1 so that )
            rScore = 1 - deviation # lower deviation is better
            currRep = self.reporting_scores[witness]
            self.reporting_scores[witness] = rScore * (PARAMS.velocity) + currRep * (1-PARAMS.velocity)


class Model:
    def __init__(self, nRSUs=1):
        # 270 status 0, 15 status 1, 10 status 2, 5 status 3
        # Decide how many AVs of each type (not random -> could use proportions later on in the simulation)
        # 90% good vehicles and 10% malicous vehicles
        nAVs = PARAMS.numVehicles
        propNormal = PARAMS.propNormal
        numNORM = int(round(nAVs*propNormal))
        numMAL, numMAL_OP, numMAL_REP = 0, 0, 0
        if PARAMS.useMalOp and not PARAMS.useMalRep:
            numMAL = int(round(nAVs*((1-propNormal)/2)))
            numMAL_OP = int(round(nAVs*((1-propNormal)/2)))
        elif PARAMS.useMalOp and PARAMS.useMalRep:
            numMAL = int(round(nAVs*((1-propNormal)/2)))
            numMAL_REP = int(round(nAVs*((1-propNormal)/2)))
        elif PARAMS.useMalOp and PARAMS.useMalRep:
            numMAL = int(round(nAVs*((1-propNormal)/3)))
            numMAL_OP = int(round(nAVs*((1-propNormal)/3)))
            numMAL_REP = int(round(nAVs*((1-propNormal)/3)))
        else:
            numMAL = int(round(nAVs*(1-propNormal)))
        statuses = [0]*numMAL + [1]*numNORM + [2]*numMAL_OP + [3]*numMAL_REP

        # implement other statues
        self.AVs = [AV(self, f"AV_{i}", statuses[i]) for i in range(nAVs)]
        self.nAVs = self.AVs[:numNORM] # normal AVs
        self.mAVs = self.AVs[numNORM:] # malicious AVs

        self.RSUs = [RSU(self, f"RSU_{i}") for i in range(nRSUs)]
        # self.current_tick = 0
    
    def initialize_reputations(self):
        for r in self.RSUs:
            r.operating_scores = {av: 1.0 for av in self.AVs} # give each av a default of 1.0
            r.reporting_scores = {av: 1.0 for av in self.AVs} 
    
    def plotScores(self, showOperating=True, showReporting=True):
        oScores = self.RSUs[0].operating_scores
        rScores = self.RSUs[0].reporting_scores

        X = [str(i) for i in oScores.keys()]

        X_axis = np.arange(len(X))

        y1 = list(oScores.values()) 
        y2 = list(rScores.values()) 

        if showOperating: plt.bar(X_axis - 0.2, y1, 0.4, label = 'Operating')
        if showReporting: plt.bar(X_axis + 0.2, y2, 0.4, label = 'Reporting')

        plt.xticks(X_axis, X, rotation=90)
        plt.xlabel("Vehicles")
        plt.ylabel("Score")
        plt.title("AV Operating and Reporting Scores")
        plt.legend()
        plt.show()



    def calculateOperatingError(self):
        err = 0
        op_scores = self.RSUs[0].operating_scores
        for av in op_scores:
            expectedRep = 1 if av.status in [1, 3] else 0 # for normal and malicious operating vehicles, their expected operating reputation is 1
            err += abs(expectedRep - op_scores[av]) # compute difference between expected score and actual reputation 
        return err / len(op_scores) # get average difference

    def calculateReportingError(self):
        err = 0
        re_scores = self.RSUs[0].reporting_scores
        for av in re_scores:
            expectedRep = 1 if av.status in [1, 2] else 0 # for normal and malicious reporting vehicles, their expected reporting reputation is 1
            err += abs(expectedRep - re_scores[av]) # compute difference between expected score and actual reputation
        return err / len(re_scores) # get average difference

    def turn(self):
        prob = random.random()
        if prob < PARAMS.percTransaction:
            if prob > (PARAMS.percTransaction - PARAMS.percMalicious):
                av = random.choice(self.mAVs) # pick a malicious AV
            else:
                av = random.choice(self.nAVs) # pick a normal AV
            # TO-DO: move recipient selection into av.broadcast
            nRecipients = int(random.random()*(PARAMS.maxRecipients-PARAMS.minRecipients)+PARAMS.minRecipients)
            recipients = random.sample([v for v in self.AVs if v is not av], nRecipients) # pick recipients as long as they aren't the sender
            av.broadcast(recipients)

    def run(self, print_error=True):
        # include runtime
        start = time.time()
        self.initialize_reputations()
        for i in range(PARAMS.numTurns):
            self.turn()
        # for (int i = 0; i < n_days; i++){ broadcast ()}
        if print_error:
            print(f"Operating Error: {self.calculateOperatingError()}")
            print(f"Reporting Error: {self.calculateReportingError()}")
        end = time.time()
        self.runtime = end-start
    
    def save_output(self, filename="output.csv"):
        newFile = False
        if not os.path.exists(filename):
            newFile = True
        with open(filename, "a") as f:
            if newFile:
                f.write("runtime,velocity,byWitnessRep,byNumWitnesses,kNumWitnesses,useQuartiles,numVehicles,minRecipients,maxRecipients,propWitnesses,propNormal,broadcastNoise,witnessNoise,useMalOp,useMalRep,numTurns,percTransaction,percMalicious,operatingScores,reportingScores")
            out = []
            out.append("\n" + str(self.runtime))
            out.append(str(PARAMS))
            out.append(f"\"{self.RSUs[0].operating_scores}\"")
            out.append(f"\"{self.RSUs[0].reporting_scores}\"")
            f.write(",".join(out))
        



model = Model() # start off with 1 rsu
model.run(print_error=False)
# scores = model.RSUs[0].operating_scores
# print(scores)
# print("Runtime:", model.runtime, "seconds")
model.save_output()
# model.plotScores()
