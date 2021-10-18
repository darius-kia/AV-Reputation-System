import random
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
import os

OPPOSITE = {1: 0, 0: 1}
STATUSES = {0: 'MAL', 1: 'NORM', 2: 'MAL_OP', 3: 'MAL_REP'}

PARAMS = []

# 0: velocity
# 1: byWitnessRep
# 2: byNumWitnesses
# 3: propNormal
# 4: broadcastNoise
# 5: witnessNoise
# 6: numVehicles
# 7: minRecipients
# 8: maxRecipients
# 9: propWitnesses
# 10: useMalOp
# 11: useMalRep
# 12: useQuartiles
# 13: numTurns
# 14: percTransaction
# 15: percMalicious

args = sys.argv[1:]
assert(len(args) > 16 or len(args) == 0), "Must include all arguments"
if len(args) == 0: # set default values
    PARAMS = [
        0.95, # 0
        True, # 1
        True,
        0.9,
        0.05,
        0.05,
        30,
        10,
        20,
        0.5,
        True,
        True,
        False,
        2000,
        0.9,
        0.1
    ]
else:
    PARAMS = args


# class Params:
#     def __init__(self, velocity, byWitnessRep, byNumWitnesses, propNormal, broadcastNoise, witnessNoise, numVehicles, minRecipients, maxRecipients, propWitnesses, useMalOp, useMalRep, useQuartiles, numTurns, percTransaction, percMalicious):
#         self.velocity = velocity
#         self.byWitnessRep = byWitnessRep
#         self.byNumWitnesses = byNumWitnesses
#         self.propNormal = propNormal
#         self.broadcastNoise = broadcastNoise
#         self.witnessNoise = witnessNoise
#         self.numVehicles = numVehicles
#         self.minRecipients = minRecipients
#         self.maxRecipients = maxRecipients
#         self.propWitnesses = propWitnesses
#         self.useMalOp = useMalOp
#         self.useMalRep = useMalRep
#         self.useQuartiles = useQuartiles
#         self.numTurns = numTurns
#         self.percTransaction = percTransaction
#         self.percMalicious = percMalicious


class AV:
    def __init__(self, model, vID, status):
        self.model = model
        self.vID = vID
        self.status = status

    def __repr__(self):
        return self.vID + f"({STATUSES[self.status]})"

    def broadcast(self, recipients, noise=PARAMS[4]):
        witnesses = random.sample(recipients, int(len(recipients)*random.random()*PARAMS[9]+1)) # picks n number of witnesses where n is between 0 and k% of the recipients
        r = random.choice(self.model.RSUs) # pick a random RSU
        transaction = {} # key is witness, value is witness's score

        expectedValue = 1 if self.status in [1, 3] else 0
        if random.random() < noise:
            expectedValue = OPPOSITE[expectedValue]
        for w in witnesses:
           transaction[w] = w.score(self, expectedValue) # have each witness score the transaction
        r.addTransaction(transaction)
        r.updateOperatingRep(self, transaction, 0.05, True, True)
        for w in witnesses:
           r.updateReportingRep(w, transaction, 0.05, weightWitnessRep=True) # update the reputation of each witness

    def score(self, sender, expected, quartiles=PARAMS[12], noise=PARAMS[5]):
        #score must take into account the status of the AV that is witnessing the transaction
        # score = random.choice([0, 1]) # make it depend on status
        # if a vehicle that is scoring a transaction has its reputation fall below 0.4 disregards the scoring from the vehicle
        scores = [0, 0.25, 0.5, 0.75, 1.0]
        wScore = -99
        if quartiles:
            wScore = expected if self.status in [1, 2] else OPPOSITE[expected]
            if random.random() < noise:
                wScore = random.choice([i for i in scores if i != wScore])
        else:
            wScore = expected if self.status in [1, 2] else OPPOSITE[expected]
            if random.random() < noise:
                wScore = OPPOSITE[wScore]
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
        self.avgWitnesses = ((self.avgWitnesses * len(self.transactions)) + len(newT)) / (len(self.transactions) + 1)
        # note: does not update prior transactions
        self.transactions.append(newT)

    def updateOperatingRep(self, sender, transaction, velocity, weightWitnessRep=PARAMS[1], weightNumWitnesses=PARAMS[2]):
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
        

    def updateReportingRep(self, witness, transaction, velocity=PARAMS[0], weightWitnessRep=True, quartiles=PARAMS[12]):
        # Calculate the average score based on the same method as used in Operating Reputation
        # 0.2 rep vehicle (malicious) reports 0 on a good transaction and 0.9 rep vehicle (non-malicious) reports 1 on a good transaction
        if quartiles:
           rRep = sum([transaction[w] for w in transaction.keys()])/len(transaction.keys())
           snapped = round(rRep*4)/4
           match = 1 if snapped == transaction[witness] else 0
           currRep = self.reporting_scores[witness]
           self.reporting_scores[witness] = match * velocity + currRep * (1-velocity)
 
        else:
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
    def __init__(self, nAVs=PARAMS[6], nRSUs=1, propNormal=PARAMS[3]):
        # 270 status 0, 15 status 1, 10 status 2, 5 status 3
        # Decide how many AVs of each type (not random -> could use proportions later on in the simulation)
        # 90% good vehicles and 10% malicous vehicles
        numNORM = int(round(nAVs*propNormal))
        numMAL = int(round(nAVs*((1-propNormal)/3)))
        numMAL_OP = int(round(nAVs*((1-propNormal)/3)))
        numMAL_REP = int(round(nAVs*((1-propNormal)/3)))
        statuses = [1]*numNORM + [0]*numMAL + [2]*numMAL_OP + [3]*numMAL_REP
        # implement other statues
        self.AVs = [AV(self, f"AV_{i}", statuses[i]) for i in range(nAVs)]
        self.nAVs = self.AVs[:numNORM] # normal AVs
        self.mAVs = self.AVs[numNORM:] # malicious AVs

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
            expectedRep = 1 if av.status in [1, 3] else 0
            err += abs(expectedRep - op_scores[av])
        return err / len(op_scores)

    def calculateReportingError(self):
        err = 0
        re_scores = self.RSUs[0].reporting_scores
        for av in re_scores:
            expectedRep = 1 if av.status in [1, 2] else 0
            err += abs(expectedRep - re_scores[av])
        return err / len(re_scores)

    def turn(self):
        prob = random.random()
        if prob < PARAMS[14]:
            if prob > (PARAMS[14]-PARAMS[15]):
                av = random.choice(self.mAVs) # pick a malicious AV
            else:
                av = random.choice(self.nAVs) # pick a normal AV
            # move recipient selection into av.broadcast
            nRecipients = int(random.random()*(PARAMS[8]-PARAMS[7])+PARAMS[7])
            recipients = random.sample([v for v in self.AVs if v is not av], nRecipients) # pick recipients as long as they aren't the sender
            av.broadcast(recipients)

    def run(self, n_turns=PARAMS[13], print_error=True):
        # include runtime
        start = time.time()
        self.initialize_reputations()
        for i in range(n_turns):
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
                print("hi")
                f.write("runtime,velocity,byWitnessRep,byNumWitnesses,propNormal,broadcastNoise,witnessNoise,numVehicles,minRecipients,maxRecipients,propWitnesses,useMalOp,useMalRep,useQuartiles,numTurns,percTransaction,percMalicious,operatingScores,reportingScores")
            out = []
            out.append("\n" + str(self.runtime))
            out.append(",".join([str(p) for p in PARAMS]))
            out.append(f"\"{self.RSUs[0].operating_scores}\"")
            out.append(f"\"{self.RSUs[0].reporting_scores}\"")
            f.write(",".join(out))
        


model = Model(33, 1, 0.9) # start off with 1 rsu
model.run(2000)
# scores = model.RSUs[0].operating_scores
print("Runtime:", model.runtime, "seconds")
model.save_output()
model.plotScores()