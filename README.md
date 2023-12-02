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

