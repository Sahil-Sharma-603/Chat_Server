
# Chat Server


## Steps to Run a program

1. **Open a Terminal**  
   Open a terminal in mac or command line in windows machine.

2. **Open Additional Terminal Windows**  
   Open two more terminal windows or command line windows.

3. **Start the Server**  
   In the first terminal window, start the server by running: ``` python3 backend.py```

The server will start and print a message showing the port number, indicating it is waiting for client input.

4. **Run the Frontend Client**  
In another terminal window, navigate to the appropriate directory and run `frontend.py` with: 
``` python3 frontend.py Username hostname port```


### Parameters:
- **Username**: Replace `<Username>` with a name to identify the client (e.g., `person1`).
- **Hostname**: Use `localhost` if you are connecting to the same machine, or provide the hostname of the server.
- **Port**: Replace `<Port>` with the port number provided by the server (e.g., `8756`).

### Example Command
To run the frontend as `person1` on localhost with port `8756`, use: ``` python3 frontend.py Person1 localhost 8756```
