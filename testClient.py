import socket
import sys
import select
import time

Username = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])

# create a TCP socket with statement - 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    print(f"Connected to the host {HOST} at port {PORT}")
    print("Type quit to exit the chat")
    startTime = time.time()

   # sending messages to server and having back and forth chat until quit is enter by client
   # infinite loop until it breaks 
    while True:
       
       message = "this is a test"
       elapsed_time = time.time() - startTime
       # after 5 minutes the while loop breaks
       if elapsed_time > 300:
        print("times up")
        sys.exit(0)
       else:
        s.sendall(f'{Username}: {message}'.encode('utf-8'))

       

        # select statement for client - blocking on select
        readable, writable, exceptional = select.select([s],[],[])

        for client in readable:
            # receving message from sever and printing
            if client is s: # client  is in s then we receive data
    
                data = s.recv(1024)
            
                if data:
                    print(data.decode("utf-8"))
                else: # exit system when server gets disconnected.
                    sys.exit(0)
                    
              
               



                
                    
            
                

# problems
# interleaving of message
# storage of message  - done
# make file
# handin
# testing


# now i can save message that are sent by the clients and show messages that previous message

# problem is now interface


    

