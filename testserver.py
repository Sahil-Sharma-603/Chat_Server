
import socket
import sys
import select
import traceback

HOST = ''                
PORT = 8756             
count_recMess = 0
count_sentMess = 0
print(f'Received Counter : {count_recMess}')
print(f'Sent Counter : {count_sentMess}')
# created TCP Socket with internet address family
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT)) # server is bound to the specific host
    s.listen() # server will start listening for incoming sections


    clients = [] # clients is the empty list that will hold connected clients sockets
    print(f"Ther server is running on port {PORT}")
    print("waiting for input")

    # main loop true foreover - infinite loop to handle the incoming connections and messages
    while True:
        try:
            inputs = [s] + clients  # input is the list of sockets that server is monitoring for incoming data
            
            readable, writable, exceptional = select.select(inputs, [], inputs)

            # handling the incoming connections - 
            for client in readable:

                #*********** Handling incoming connections ****************
                # if client is the server socket s,  it means new client is trying to connect.
                if client is s:
                
                    # s.accept() will accept the new connection 
                    # returning new socket connection (con) and the address of the client(addr)
                    conn, addr = s.accept()
                    print('Connected by', addr)
                    clients.append(conn) # the new client is added to the clients list 
    
                    # then need to send the stored message first to all the clients connected to the server
                    try:
                        with open('store_message_test.txt', 'r') as f:
                            content = f.read()
                            conn.sendall(content.encode('utf-8'))
                    except:
                        print("File not found")

                   # ******* Handling messages from clients **************
                # if statement - for existing clients, server receives data 
                # and it read upto 1024 bytes from the socket
                # if client in clients:     
                else: # receving data from client 
                    data = client.recv(1024)
                    message = data.decode("utf-8").strip()
                    count_recMess += 1
                    print(f'Message received from client: {count_recMess}')
                    print(message) # getting data in format username: message and sending data in same format

                    # count the messages recieve from client or clients -
                    


                    # store a data which is receive from clients in a file 
                    with open('store_message_test.txt', 'a') as f:
                        f.write(message + '\n')


                    if data: # now sending data to all other clients that connected and it is in the list 
                        for client_sock in clients:

                            #if client_sock is not client:
                                client_sock.sendall(data)
                                count_sentMess  += 1
                                print(f'Message sent from server: {count_sentMess}')
    
                    else:
                        message = input().strip()
                         if message.lower() == 'quit':
                         sys.exit(0)
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


