from db import *
from model import *
import logging
import threading
import time
from datetime import datetime
import os


# def thread_function(name):
#     testBlock = Block(datetime.now(), ['t1', 't2', 't3'], '240n4568a40f5670824m0af4ln280')
#     print(testBlock)
#     diff = 4
#     print(f"Start (PoW difficulty of {diff}):")
#     testBlock.mineBlock(diff)
#     print("Done:", testBlock.hash)
#     os._exit(os.EX_OK)

# if __name__ == "__main__":
#     x = threading.Thread(target=thread_function, args=(1,))
#     x.start()
#     # x.join()
#     i = 0
#     while True:
#         print(i)
#         time.sleep(1)
#         i += 1

    # blockchain = Blockchain(2, 10)
    # model = Model()
    # av1 = AV(None, "AV_1", 1)
    # av2 = AV(None, "AV_2", 1)
    # print(blockchain.chain)

minerAddress = "RSU1"
user1Address = "AV1"
user2Address = "AV2"

blockchain = Blockchain(2, 10)
blockchain.printChain()
print("############")
blockchain.createTransaction(Transaction(user1Address, user2Address, "test"))
blockchain.printChain()
print(blockchain.isValidChain())
blockchain.mineBlock(minerAddress)
print("#########")
print(len(blockchain.chain))