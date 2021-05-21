import socket
import pickle
import Transactions
import TxBlock
import select

TCP_PORT = 5005
buffer_size = 1024


def newServerConnection(ip_addr, port = TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr,port))
    s.listen()
    return s

def sendObj(ip_addr, inObj, port = TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr, port))
    data = pickle.dumps(inObj)
    s.send(data)
    s.close()
    return False

def recvObj(socket):
    #     This will fix the issue of waiting/accepting
    inputs,outputs,errors = select.select([socket],[],[socket],6)
    if inputs:
        new_sock,addr = socket.accept() 
        data = b""
        while True:
            packet = new_sock.recv(buffer_size)
            if not packet: 
                break
            data += packet
        return pickle.loads(data)
    return None
if __name__ == "__main__":
    server = newServerConnection('localhost')
    O = recvObj(server)
    print("success!")
    server.close()