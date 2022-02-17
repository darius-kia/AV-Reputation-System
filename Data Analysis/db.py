from hashlib import sha256
from datetime import datetime

class Transaction:
    def __init__(self, avFrom, avTo, amount):
        self.avFrom = avFrom
        self.avTo = avTo
        self.amount = amount # may be removed

class Block:
    def __init__(self, timestamp, transactions, previousHash):
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.createHash()
    def mineBlock(self, proofOfWorkDifficulty):
        hashValidationTemplate = '0'*proofOfWorkDifficulty
        while self.hash[0:proofOfWorkDifficulty] != hashValidationTemplate:
            self.nonce += 1
            self.hash = self.createHash()
    def createHash(self):
        # print(self.nonce)
        raw_data = self.previousHash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        h = sha256(raw_data.encode('utf-8')).hexdigest()
        # print(h)
        return h

class Blockchain:
    def __init__(self, proofOfWorkDifficulty, miningReward):
        self.proofOfWorkDifficulty = proofOfWorkDifficulty
        self.miningReward = miningReward
        self.pendingTransactions = [] # fill with Transaction objects
        self.chain = [] # may be revised

    def createTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def mineBlock(self, minerAddress):
        minerRewardTransaction = Transaction(None, minerAddress, self.miningReward)
        self.pendingTransactions.append(minerRewardTransaction)

        block = Block(datetime.now(), self.pendingTransactions)
        block.mineBlock(self.proofOfWorkDifficulty)

        block.previousHash = self.chain[-1].hash
        self.chain.append(block)

        self.pendingTransactions = []
    
    def isValidChain(self):
        for i in range(1, len(self.chain)):
            previousBlock = self.chain[i-1]
            currentBlock = self.chain[i]

            if currentBlock.hash != currentBlock.createHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False

        return True

    def createGenesisBlock(self):
        transactions = [Transaction("", "", 0)]
        return Block(datetime.now(), transactions, "0")


testBlock = Block(23, '240n4568a40f5670824m0af4ln280', ['t1', 't2', 't3'])
print(testBlock.hash)
testBlock.mineBlock(4)
