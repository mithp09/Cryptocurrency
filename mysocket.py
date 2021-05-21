# Socket communication
# TCP - need to create a connection and only then you can use it 
#     - will know if your package has been delivered 

# The server will bind the port number; therefore, you do not need to create a port for the client

import socket

ip_addr = '192.168.0.39'
port = 5005

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((ip_addr,port))

# The argument = number of people you want to connect
s.listen()
print('Waiting for connection')

for q in range(10):
        #    Accept will split out the client's socket and address
# The issue is accept is that it will be waiting for a connection to accept, which will prevent other code from running 
    rd,wt,err = select.select([s],[],[s],6) # 6 is the 6 sec timeout 
    
#     The accept will only activate if there is something to read (rd)
    if rd:
#    Accept will split out the client's socket and address
        c, addr = s.accept()

        while True:
            data = conn.recv()
    
#     client will send empty string indicating to end communication
            if not data:
                break
            print("Rec'd: " + data)
    
#     Sending needs to be in byte format
            conn.send(data) # Since echo communication, you want to send data back.
        s.close()
        
        
# Creating client connection here

c = socket.socket()

c.connect(('Localhost', 5005))

c.send(bytes('Mithil','utf-8'))

# To receive messages
print(c.recv(1024)) # 1024 is the buffer size and .decode() is to convert bytes to string
c.close()

