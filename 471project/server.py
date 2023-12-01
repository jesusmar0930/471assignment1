import socket
import os
import hashlib
import sys
import time 

def calculate_file_hash(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"FTP Server is running on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

def handle_client(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                print("Client disconnected.")
                break

            try:
                if command.lower().startswith('ls'):
                    handle_ls_command(client_socket)
                    client_socket.send("LS command executed successfully.\n".encode())
                elif command.lower().startswith('get'):
                    handle_get_command(client_socket, command)
                    client_socket.send("GET command executed successfully.\n".encode())
                elif command.lower().startswith('put'):
                    handle_put_command(client_socket, command)
                    client_socket.send("PUT command executed successfully.\n".encode())
            
            except Exception as cmd_error:
                print(f"Error executing command '{command}': {cmd_error}")
                client_socket.send(f"Error: {cmd_error}\n".encode())

    except OSError as e:
        if e.winerror == 10054:
            print("Connection forcibly closed by client.")
        else:
            print(f"Socket error: {e}")
    finally:
        client_socket.close()
        print("Client connection closed.")


def handle_ls_command(client_socket):
    print("Executing 'ls' command...")
    files = os.listdir('.')
    files_list = '\n'.join(files) + '\nEND_OF_LS'
    client_socket.sendall(files_list.encode())
    print("File list sent to client.")

def handle_get_command(client_socket, command):
    print(f"Handling GET command: {command}")
    data_socket = None

    try:
        _, filename, data_port = command.split()
        data_port = int(data_port)  # Convert to integer
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the client's data port
        data_socket.connect((client_socket.getpeername()[0], data_port))
        print(f"Establishing data connection on port {data_port}")

        # Open and read the file, then send it to the client
        with open(filename, 'rb') as file:
            while True:
                bytes_read = file.read(1024)
                if not bytes_read:
                    break
                data_socket.sendall(bytes_read)

        # Send file hash for checksum verification
        file_hash = calculate_file_hash(filename)
        data_socket.sendall(b'END' + file_hash.encode())
        print(f"Checksum for sent file: {file_hash}")

    except FileNotFoundError:
        print("Error: File not found.")
        if data_socket:
            data_socket.send(b"Error: File not found")
    except Exception as e:
        print(f"Error in GET command: {e}")
    finally:
        if data_socket:
            data_socket.close()
            print("Data connection closed.")


def handle_put_command(client_socket, command):
    _, filename, data_port = command.split()
    data_port = int(data_port)
    data_socket = None  # Initialize the variable

    try:
        # Establish a connection to the client's data port
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((client_socket.getpeername()[0], data_port))

        # Receiving file from the client
        file_data = bytearray()
        while True:
            data = data_socket.recv(1024)
            if b'END' in data:
                file_data.extend(data.split(b'END')[0])
                break
            file_data.extend(data)

        with open(filename, 'wb') as file:
            file.write(file_data)

        # Receive and calculate checksum
        received_checksum = data_socket.recv(1024).decode()
        calculated_checksum = hashlib.md5(file_data).hexdigest()
        print(f"Checksum for received file: {calculated_checksum}")

        if received_checksum == calculated_checksum:
            print(f"File {filename} received successfully with matching checksum.")
        else:
            print(f"Checksum mismatch for {filename}.")

    except Exception as e:
        print(f"Error in PUT command: {e}")
    finally:
        if data_socket:
            data_socket.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 21

    start_server(port)
