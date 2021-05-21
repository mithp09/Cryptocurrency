import Socketutil
import Transactions
import TxBlock
from Signatures import generate_keys
from Blockchain import CBlock
import threading
import time

wallets = [('localhost'),5005]
tx_list = []
head_blocks = [None]
break_now = False
def findLongestBlockchain():
    longest = -1
    long_head = None
    for b in head_blocks:
        current = b
        this_len = 0
        while current != None:
            this_len += 1
            current = current.previousBlock 
        if this_len > longest:
            longest = this_len
            long_head = b
    return long_head
def minerServer(my_addr):
    global tx_list
    global break_now
    my_ip, my_port = my_addr
    #open Server Connection
    server = Socketutil.newServerConnection(my_ip,my_port) 
    # Rec'v 2 transactions
    while not break_now:
        newTx = Socketutil.recvObj(server)
        if isinstance(newTx,Transactions.Tx):
            tx_list.append(newTx)
            print("Recd tx")
    return False

def nonceFinder(wallet_list,miner_public):
    # Add txs to block
    global break_now
    while not break_now:
        newBlock = TxBlock.TxBlock([],findLongestBlockchain())
        for tx in tx_list:
            newBlock.addTx(tx)
    
       # Compute and add mining reward
        total_in,total_out = newBlock.count_totals()
        mine_reward = Transactions.Tx()
        mine_reward.add_output(miner_public,25.0+total_in-total_out)
        newBlock.addTx(mine_reward)
    # Find nonce
        print ("Finding Nonce...")
        newBlock.find_nonce(10000)
        if newBlock.good_nonce():
            print ("Good nonce found")
            # Send new block
            for ip_addr,port in wallet_list:
                print ("Sending to " + ip_addr + ":" + str(port))
                Socketutil.sendObj(ip_addr,newBlock,5006)
            head_blocks.remove(newBlock.previousBlock)
            head_blocks.append(newBlock)
            break
        return True 

if __name__ == '__main__': 
    my_pr, my_pu = generate_keys()
    t1 = threading.Thread(target = minerServer, args = (('localhost',5005),))
    t2 = threading.Thread(target = nonceFinder, args = (wallets,my_pu))
    server = Socketutil.newServerConnection('localhost', 5006)
    t1.start()
    t2.start()
    
    pr1,pu1 = generate_keys()
    pr2,pu2 = generate_keys()
    pr3,pu3 = generate_keys()

    Tx1 = Transactions.Tx()
    Tx2 = Transactions.Tx()
    
    Tx1.add_input(pu1, 4.0)
    Tx1.add_input(pu2, 1.0)
    Tx1.add_output(pu3, 4.8)
    Tx2.add_input(pu3, 4.0)
    Tx2.add_output(pu2, 4.0)
    Tx2.add_reqd(pu1)

    Tx1.sign(pr1)
    Tx1.sign(pr2)
    Tx2.sign(pr3)
    Tx2.sign(pr1)

    try:
        Socketutil.sendObj('localhost',Tx1)
        print('Sent Tx1')
        Socketutil.sendObj('localhost',Tx2)
        print("Send Tx2")
    except:
        print ("Error! Connection unsuccessful")
    for i in range(10):
        newBlock = Socketutil.recvObj(server)
        if newBlock:
            break
    
    if newBlock.is_valid():
        print("Success! Block is valid")
    
    if newBlock.good_nonce():
        print("Success! Nonce is valid")
    for tx in newBlock.data:
        try:
            if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
                print("Tx1 is present")
        except:
            pass
        try:
            if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
                print("Tx2 is present")
        except:
            pass
    time.sleep(20)
    break_now = True
    time.sleep(2)
    server.close()
    
    t1.join()
    t2.join()
    
    print("Done")
