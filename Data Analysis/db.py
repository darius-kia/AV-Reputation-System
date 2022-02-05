from hashlib import sha256

class Block:
    def __init__(self, timestamp, previousHash, transactions):
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
        print(self.nonce)
        raw_data = self.previousHash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        h = sha256(raw_data.encode('utf-8')).hexdigest()
        return h


testBlock = Block(23, '240n4568a40f5670824m0af4ln280', ['t1', 't2', 't3'])
print(testBlock.hash)
