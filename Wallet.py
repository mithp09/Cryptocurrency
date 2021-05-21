import Socketutil
import Transactions
import Signatures
import time
import Miner
import threading
import TxBlock

head_blocks = [None]
wallets = [('localhost',5006)]
miners = [('localhost',5005)]
break_now = False

def walletServer(my_addr):
#     responsible for building a block 
    server = Socketutil.newServerConnection('localhost',5006)
    while not break_now:
        newBlock = Socketutil.recvObj(server)
        if isinstance(newBlock, TxBlock.TxBlock):
            for b in head_blocks:
                if b.previousBlock == None:
                    if newBlock.previous == None:
                        newBlock.previousBlock = b
                        if not newBlock.is_valid():
                            print("Error! newBlock is not valid")
                        else:
                            head_blocks.remove(b)
                            head_blocks.append(newBlock)
                            print("Added to the block ")
    
                if newBlock.previousHash == b.computeHash():
                    newBlock.previousBlock = b
                    if not newBlock.is_valid():
                            print("Error! newBlock is not valid")
                        else:
                            head_blocks.remove(b)
                            head_blocks.append(newBlock)
                            print("Added to the block ")
    server.close()
    return True

def getBalance(pu_key):
    return 0.0

def sendCoins(pu_send, amt_send, pr_send, pu_recv, amt_recv, miner_list):
    newTx = transactions. Tx()
    newTx.add_input(pu_send, amt_send)
    newTx.add_output(pu_recv,amt_recv)
    newTx.sign(pr_send)
     
    Socketutil.sendObj('localhost',Tx1)
    return True

if __name__ == "__main__":
    
    miner_pr, miner_pu = Signatures.generate_keys()
    t1 = threading.Thread(target=Miner.minerServer, args=(('localhost',5005),))
    t2 = threading.Thread(target=Miner.nonceFinder, args=(wallets, miner_pu))
    t3 = threading.Thread(target=walletServer, args=(('localhost',5006),))
    t1.start()
    t2.start()
    t3.start()

    pr1,pu1 = Signatures.generate_keys()
    pr2,pu2 = Signatures.generate_keys()
    pr3,pu3 = Signatures.generate_keys()

    #Query balances
    bal1 = getBalance(pu1)
    bal2 = getBalance(pu2)
    bal3 = getBalance(pu3)

    #Send coins
    sendCoins(pu1, 1.0, pr1, pu2, 1.0, miners)
    sendCoins(pu1, 1.0, pr1, pu3, 0.3, miners)

    time.sleep(30)

    #Query balances
    new1 = getBalance(pu1)
    new2 = getBalance(pu2)
    new3 = getBalance(pu3)

    #Verify balances
    if abs(new1-bal1+1.3) > 0.00000001:
        print("Error! Wrong balance for pu1")
    else:
        print("Success. Good balance for pu1")
    if abs(new2-bal2-1.0) > 0.00000001:
        print("Error! Wrong balance for pu2")
    else:
        print("Success. Good balance for pu2")
    if abs(new3-bal3-0.3) > 0.00000001:
        print("Error! Wrong balance for pu3")
    else:
        print("Success. Good balance for pu3")

    Miner.break_now=True
    break_now = True
    
    t1.join()
    t2.join()
    t3.join()

    print ("Exit successful.")