import random

class AV:
    def __init__(self, model, vID, status):
        self.model = model
        self.vID = vID
        self.status = status
    
    def broadcast(message, recipients):
        pass

    def witness(message):
        pass

class RSU:

    def __init__(self, model, rID):
        self.model = model
        self.rID = rID
        self.reputation_scores = {} # list of dictionaries
    
    def addReputationScore(self, vehicleA, vehicleB, score):
        cur_scores = dict()
        
        if vehicleA in reputation_scores:
            cur_dict = reputation_scores[vehicleA]
            
            if vehicleB in cur_dict:
                cur_scores = cur_dict[vehicleB]
            
            cur_scores.append(score)
            cur_dict[vehicleB] = cur_scores
            reputation_scores[vehicleA] = cur_dict
        else:
            cur_scores[vehicleB] = [score]
            reputation_scores[vehicleA] = cur_scores


class Model:
    def __init__(self, n):
        self.nodes = [AV(self, i, random.randint(0, 3)) for i in range(n)]

model = Model(300)