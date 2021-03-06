 # Secure,public Ledger
from Blockchain import CBlock
from Signatures import generate_keys, sign, verify
from Transactions import Tx
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import random
from cryptography.hazmat.primitives import hashes
import time
reward = 25.0
leading_zeros = 2
next_char_limit = 100

class TxBlock(CBlock):
    nonce = "AAAAAAA"
    def __init(self, previousBlock):
        super(TxBlock,self).__init__([],previousBlock)
    def addTx(self, Tx_in):
        self.data.append(Tx_in)
    def count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr,amt in tx.inputs:
                total_in = total_in + amt
            for addr,amt in tx.outputs:
                total_out = total_out + amt          
        return total_in,total_out
    def is_valid(self):
        if not super(TxBlock,self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False 
#         To avoid floating point error ( 0.2 + 0.4 = .600000000001), see the code below
        total_in,total_out = self.count_totals() 
        if total_out - total_in - reward > 0.000000000001:
            return False
        return True

#     Nonce = occasion or to verify the transaction has happened once 
    def good_nonce(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        digest.update(bytes(str(self.nonce),'utf8'))
        this_hash = digest.finalize()
        
#         generates a code of leading zeros 
        if this_hash[:leading_zeros] != bytes(''.join([ '\x4f' for i in range(leading_zeros)]),'utf8'):
            return False
        return int(this_hash[leading_zeros]) < next_char_limit
        
    def find_nonce(self,n_tries = 10000000):
        for i in range(10000000):
            self.nonce = ''.join([ 
                   chr(random.randint(0,255)) for i in range(10*leading_zeros)])
            if self.good_nonce():
                return self.nonce  
        return None

if __name__=='__main__':
    pr1,pu1 = generate_keys()
    pr2,pu2 = generate_keys()
    pr3,pu3 = generate_keys()
    
    Tx1 = Tx()
    Tx1.add_input(pu1,1)
    Tx1.add_output(pu2,1)
    Tx1.sign(pr1)
    
    if Tx1.is_valid():
        print('Successs! Tx is valid')

#     Storing blockchain to a disc using pickle
# Pickle serializes data and stores, which can later to be instead of train the whole model again
# pickle.dump(data -> serialize)..... pickle.load(serialize -> data), which you can print from
#     message = b'Some text'
#     sig = Signatures.sign(message, pr1)

#     wb = binary writing
    
#  You cannot pickle public and private key since the are coded using different lang; Therefore,
#  you need to serialize using the code below 
#     pu_ser = pu1.public_bytes(
#        encoding=serialization.Encoding.PEM,
#        format=serialization.PublicFormat.SubjectPublicKeyInfo
#      )
#     pickle can dump as string or binary 
    savefile = open('tx.dat','wb')
    pickle.dump(Tx1,savefile)
    savefile.close()
        
    loadfile = open('tx.dat','rb')
    newTx = pickle.load(loadfile)
    
# This is to deserialize the public key
#     loaded_pu = serialization.load_pem_public_key(
#             new_pu,
#         backend = default_backend()
#     ) 
    if newTx.is_valid():
        print('Success! loaded tx is valid')
    loadfile.close()
    
    root = TxBlock([],None)
    root.addTx(Tx1)
    
    Tx2 = Tx()
    Tx2.add_input(pu2,1.1)
    Tx2.add_output(pu3,1)
    Tx2.sign(pr2)
    root.addTx(Tx2)
    
    B1 = TxBlock([],root)
    Tx3 = Tx()
    Tx3.add_input(pu3,1.1)
    Tx3.add_output(pu1,1)
    Tx3.sign(pr3)
    B1.addTx(Tx3)
    
    Tx4 = Tx()
    Tx4.add_input(pu1,1.1)
    Tx4.add_output(pu2,1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.addTx(Tx4)

    start = time.time()
    print(B1.find_nonce())
    elapsed = time.time() - start
    print("elapsed time: " + str(elapsed) + " s.")
    if elapsed < 60:
        print("ERROR! Mining is too fast")
    if B1.good_nonce():
        print("Success! Nonce is good!")
    else:
        print("ERROR! Bad nonce")
        
#     B1.is_valid()
#     root.is_valid()
    
    savefile = open('block.dat','wb')
    pickle.dump(B1, savefile)
    savefile.close()
    
    loadfile = open('block.dat','rb')
    load_B1 = pickle.load(loadfile)
    
    for b in [root,B1,load_B1,load_B1.previousBlock]:
        if b.is_valid():
            print('Success! valid block')
        else:
            print('Error! Bad block')
    if B1.good_nonce():
        print("Success! Nonce is good after save and load!")
    else:
        print("ERROR! Bad nonce after load")
        
#     Invalid transaction
    B2 = TxBlock([],B1)
    Tx5 = Tx()
    Tx5.add_input(pu3,1)
    Tx5.add_output(pu1,100)
    Tx5.sign(pr3)
    B2.addTx(Tx5)
    
#     Load_B1 is invalid because it might contain same data but different location, so it doesnt match.
# Need to use the repr to print the data so it can match
    load_B1.previousBlock.addTx(Tx4)
    for b in [B2,load_B1]:
        if b.is_valid():
            print('Error! Bad block verified')
        else:
            print("Success! Bad block is detected")
    
# Miner's reward and tx fee


    pr4,pu4 = generate_keys() # generating miner's keys
    B3 = TxBlock([],B2)
    B3.addTx(Tx2)
    B3.addTx(Tx3)
    B3.addTx(Tx4)

    Tx6 = Tx() # creating a transaction for the miner to claim their reward
    Tx6.add_output(pu4,25)
    B3.addTx(Tx6)

    if B3.is_valid():
        print("sucess! Block reward succeeds")
    else:
        print('Error! Block reward failed')

#     Collecting Tx fee
    B4 = TxBlock([],B3)
    B4.addTx(Tx2)
    B4.addTx(Tx3)
    B4.addTx(Tx4)
    Tx7 = Tx()
    Tx7.add_output(pu4, 25.2) #want to collect the additional 0.1 from 1.1 - > 1 (Tx2,Tx3)
    B4.addTx(Tx6)

    if B4.is_valid():
        print("sucess! Tx fee succeeds")
    else:
        print('Error! Tx fee failed')
    
#     Greedy Miner 
    B5 = TxBlock([],B4)
    B5.addTx(Tx2)
    B5.addTx(Tx3)
    B5.addTx(Tx4)

    Tx8 = Tx() 
    Tx8.add_output(pu4,26.2) # getting extra coin 
    B5.addTx(Tx8)

    if not B5.is_valid():
        print("success! Greedy miner detected")
    else:
        print('Error! Greedy miner not detected')