import random

class AV:
    def __init__(self, model, vID, status):
        self.model = model
        self.vID = vID
        self.status = status
    
    def broadcast(message, recipients):
        witnesses = random.sample(recipients, int(len(recipients)*random.random()*0.5)) # picks n number of witnesses where n is between 0 and 50% of the recipients
        r = random.choice(self.model.RSUs) # pick a random RSU
        transaction = {} # key is witness, value is witness's score
        for w in witnesses:
           transaction[w] = w.score(self, message) # have each witness score the transaction
        r.updateOperatingRep(self, transaction)

    def score(sender, message):
        score = random.choice([0, 1]) # make it depend on status
        return score

class RSU:

    def __init__(self, model, rID):
        self.model = model
        self.rID = rID
        self.reputation_scores = {} # key is the av, value is its current reputation; should be stored by BS, RSU stores transaction info
    
    def updateOperatingRep(self, sender, transaction):
        # update the reputation of sender AV using the transaction
        # does this by iterating through the witness scores for the transaction and get weighted average
        tRep = 0
        repSum = sum([self.reputation_scores[w] for w in transaction.keys()])
        for w in transaction.keys():
            weight = self.reputation_scores[w] / repSum
            tRep += transaction[w] * weight

        currRep = self.reputation_scores[sender]
        self.reputation_scores[sender] = tRep * 0.05 + currRep * 0.95
        # TO-DO weight based on recency AND number of witnesses
        

    def updateReportingRep(self):
        pass

class Model:
    def __init__(self, nAVs, nRSUs):
        self.AVs = [AV(self, i, random.randint(0, 3)) for i in range(nAVs)]
        self.RSUs = [RSU(self, i, random.randint(0, 3)) for i in range(nRSUs)]

model = Model(300)