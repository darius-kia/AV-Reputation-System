import random

class AV:
    def _init_(self, id, status):
        self.id = id
        self.status = status


class RSU:
    # dictionary of dictionaries
    reputation_scores = {}
    
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


ids = [i for i in range(300)]
statuses = [random.randint(0, 3) for i in range(300)]
nodes = [AV(ids[i], statuses[i]) for i in range(300)]
