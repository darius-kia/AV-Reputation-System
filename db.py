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
    def __repr__(self):
        x = ""
        x += f"Timestamp: {self.timestamp}\n"
        x += f"Transactions: {len(self.transactions)}\n"
        x += f"Hash: {self.hash}"
        return x
        
    def mineBlock(self, proofOfWorkDifficulty):
        hashValidationTemplate = '0'*proofOfWorkDifficulty
        while self.hash[0:proofOfWorkDifficulty] != hashValidationTemplate:
            self.nonce += 1
            self.hash = self.createHash()
            # print(self.hash)
    def createHash(self):
        raw_data = str(self.previousHash) + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        h = sha256(raw_data.encode('utf-8')).hexdigest()
        # print(h)
        return h

class Blockchain:
    def __init__(self, proofOfWorkDifficulty, miningReward):
        self.proofOfWorkDifficulty = proofOfWorkDifficulty
        self.miningReward = miningReward
        self.pendingTransactions = [] # fill with Transaction objects
        self.chain = [self.createGenesisBlock()] # may be revised
        self.numTransactions = 1

    def addTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def mineBlock(self, minerAddress):
        minerRewardTransaction = Transaction(None, minerAddress, self.miningReward)
        self.pendingTransactions.append(minerRewardTransaction)

        block = Block(datetime.now(), self.pendingTransactions, self.chain[-1].hash)
        block.mineBlock(self.proofOfWorkDifficulty)
        print(block.hash)

        self.chain.append(block)
        self.numTransactions += len(self.pendingTransactions)
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

    def printChain(self):
        print("------------")
        for b in self.chain:
            print(b)
            print("------------")


