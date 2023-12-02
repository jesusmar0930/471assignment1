Custom File Transfer Protocol (CFTP)
CFTP is a custom implementation of a file transfer protocol.  It uses separate control and data connections to handle file transfers and directory listings.

Prerequisites
Python 3.x
Network access between the client and server (if not running on the same machine)
Installation
Clone or download the CFTP repository.
Ensure Python 3.x is installed on both the server and client machines.
Running the Server
To start the server, navigate to the directory containing server.py and run:

python server.py <PORT_NUMBER>

Replace <PORT_NUMBER> with the desired port number (e.g., 1234).
Running the Client
To connect to the server, navigate to the directory containing client.py and run:
python client.py <SERVER_IP> <PORT_NUMBER>

Replace <SERVER_IP> with the server's IP address and <PORT_NUMBER> with the port number the server is listening on.
Usage
Once the client is connected to the server, the following commands can be used:
ls: Lists all files in the server's directory.
get <filename>: Downloads <filename> from the server.
put <filename>: Uploads <filename> to the server.
quit: Disconnects the client from the server and exits.
Authors
Jesus Martinez jesus.mar0930@csu.fullerton.edu
Allan Cortes and allan.cor98@csu.fullerton.edu


Design: 
+-----------------+                            +-----------------+
|                 |      Control Channel       |                 |
|    CLIENT       +---------------------------->    SERVER       |
|                 | TCP Connection (e.g., 1234)|                 |
+--------+--------+                            +--------+--------+
         |                                               |
         |                                               |
         |                                               |
         |  (Client sends command: GET, PUT, LS, or QUIT) |
         |                                               |
         +----------------+-----------------------+-------+
                          |                       |
                          |                       |
+-------------------------v-+                   +-v----------------------+
|                          |                   |                        |
|     Data Channel         |                   |     Data Channel       |
|   (Ephemeral Port)       |                   |   (Ephemeral Port)     |
|                          |                   |                        |
+--------------------------+                   +------------------------+
     (File Transfer)                                (File Transfer)



Server pseudocode:
Procedure StartServer(port):
    Create server_socket and bind to port
    Listen for incoming connections

    While True:
        Accept incoming connection on server_socket into client_socket
        HandleClient(client_socket)

Procedure HandleClient(client_socket):
    While True:
        Receive command from client_socket
        If command is 'ls':
            HandleLsCommand(client_socket)
        ElseIf command starts with 'get':
            HandleGetCommand(client_socket, command)
        ElseIf command starts with 'put':
            HandlePutCommand(client_socket, command)
        ElseIf command is 'quit':
            Break the loop
    Close client_socket

Procedure HandleLsCommand(client_socket):
    List files in the server directory
    Send file list to client_socket

Procedure HandleGetCommand(client_socket, command):
    Parse filename from command
    Establish data connection with client
    Send file over data connection
    Close data connection

Procedure HandlePutCommand(client_socket, command):
    Parse filename and data port from command
    Establish data connection with client
    Receive file over data connection
    Close data connection



Client pseudocode:
Procedure StartClient(server_ip, port):
    Create client_socket and connect to server_ip and port

    While True:
        Display 'ftp>' prompt for user command
        If command is 'ls':
            Send 'ls' to server and display response
        ElseIf command starts with 'get':
            HandleGetCommand(client_socket, command)
        ElseIf command starts with 'put':
            HandlePutCommand(client_socket, command)
        ElseIf command is 'quit':
            Send 'quit' to server and exit
    Close client_socket

Procedure HandleGetCommand(client_socket, command):
    Send 'get' command to server
    Establish data connection as instructed by server
    Receive file from data connection
    Close data connection

Procedure HandlePutCommand(client_socket, command):
    Send 'put' command to server
    Establish data connection as instructed by server
    Send file over data connection
    Close data connection


