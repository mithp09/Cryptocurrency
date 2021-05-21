import TxBlock
import socket
import pickle

TCP_PORT = 5005
buffer_size = 1024

# creating a connection. By splitting the function, you can allow to send multiple items on same connection
def newConnection(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr,TCP_PORT))
    s.listen()
    return s

# Sending multiple data 
def recvObj(socket):
    new_sock,addr = s.accept() 
    data = b""
    while True:
        packet = new_sock.recv(buffer_size)
        if not packet: 
            break
        data += packet
    return pickle.loads(data)

if __name__ == "__main__":
    s = newConnection('localhost')
    newB = recvObj(s)
    print(newB.data[0])
    print(newB.data[1])
    
    if newB.is_valid():
        print("Success! Tx is valid.")
    else:
        print("Error! Tx is invalid.")
        
    if newB.data[0].inputs[0][1] == 2.3:
        print ("Success. Input value matches")
    else:
        print ("Error! Wrong input value for block 1, tx 1")
    if newB.data[0].outputs[1][1] == 1.1:
        print ("Success. Output value matches")
    else:
        print ("Error! Wrong output value for block 1, tx 1")
    if newB.data[1].inputs[0][1] == 2.3:
        print ("Success. Input value matches")
    else:
        print ("Error! Wrong input value for block 1, tx 1")
    if newB.data[1].inputs[1][1] == 1.0:
        print ("Success. Input value matches")
    else:
        print ("Error! Wrong input value for block 1, tx 1")
    if newB.data[1].outputs[0][1] == 3.1:
        print ("Success. Output value matches")
    else:
        print ("Error! Wrong output value for block 1, tx 1")
    
    newTx = recvObj(s)
    print(newTx)