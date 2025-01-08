#!/usr/bin/python3

# started with https://docs.python.org/3/library/socket.html#example

# chat-hopper!
# Give the message to the next person


import socket
import sys
import select
import traceback

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port 
# we can use PORT = 0 or PORT = ' ' as empty string to randomly select the port by operating system

lastWord = "F1rst p0st"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # created TCP Socket with internet address family
    # blocking, but default
    # https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts

    # socket options - This option allows the socket to be bound to an address that is in a TIME_WAIT state. 
    # It prevents the "Address already in use" error when restarting the server.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    # overall timeout
    # Q: What happens if I remove this timeout, and the other one, too?
    s.settimeout(0)

    # Bind() - TCP and UDP as well
    s.bind((HOST, PORT)) # server is bound to the specific host
    # Listen () and accept() is in only TCP not UDP
    s.listen() # server will start listening for incoming sections
    clients = [] # clients is the empty list that will hold connected clients sockets

    # main loop true foreover - infinite loop to handle the incoming connections and messages
    while True:
        try:
            inputs = [s] + clients  # input is the list of sockets that server is monitoring for incoming data
            
            # only block
            # select statement where we block - returns readable, writeable and exceptional. 
            # here only readable and exceptional is used

            readable, writable, exceptional = select.select(inputs, [], inputs)

            # handling the incoming connections - 
            for client in readable:

                #*********** Handling incoming connections ****************
                # if client is the server socket s,  it means new client is trying to connect.
                if client is s:
                
                    # s.accept() will accept the new connection 
                    # returining new socket (conn) and the address of the client(addr)
                    conn, addr = s.accept()
                    print('Connected by', addr)
                    # the new client is added to the clients list 
                    clients.append(conn)

                   # ******* Handling messages from clients **************
                # if statement - for existing clients, server receives data 
                # and it read upto 1024 bytes from the socket
                if client in clients:     
                    data = client.recv(1024)
                    print(data)
                    if data:
                        print('swapping')
                        currWord = lastWord # storing lastword in variable 
                        lastWord = data.strip() # data from client is stored in lastword now 
                        client.sendall(currWord) # sending the server message to client
                    #**********Handling disconnects **************
                    else: 
                        print("goodbye")
                        clients.remove(client) # server removes the client from the clients list
                        client.close() # it close the connection
     
        #********** Exceptional handling ****************
        except KeyboardInterrupt as e: # exit gracefully when enter ctrl+c
            print("RIP")
            sys.exit(0)
        except Exception as e:
            print("Something happened... I guess...")
            print(e)
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)


# Chat Server: This server allows multiple clients to connect and exchange messages.
# Message Swapping: Each client sends a message, and the server responds with the last received message, creating a simple chat-like interaction.
# Handling Connections: The server uses select to manage multiple client connections efficiently without blocking.
# Graceful Shutdown: The server can be stopped safely with a keyboard interrupt, and any exceptions are logged for troubleshooting.