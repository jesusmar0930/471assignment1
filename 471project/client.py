import socket
import hashlib
import sys
import time 


def calculate_file_hash(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def initiate_data_connection():
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('', 0))  # Bind to an ephemeral port
    data_port = data_socket.getsockname()[1]
    data_socket.listen(1)
    return data_socket, data_port

def handle_file_transfer(client_socket, command):
    data_socket, data_port = initiate_data_connection()
    full_command = f"{command} {data_port}"
    print(f"Sending command to server: {full_command}")  # Debug print
    client_socket.send(full_command.encode())

    print("Waiting for server to connect for data transfer...")  # Debug print
    conn, addr = data_socket.accept()
    print(f"Server connected for data transfer: {addr}")  # Debug print

    if command.startswith('get'):
        receive_file(conn, command)
    elif command.startswith('put'):
        send_file(conn, command)

    conn.close()
    data_socket.close()



def receive_file(data_socket, command):
    print("Receiving file...")
    filename = command.split()[1]
    file_data = bytearray()

    while True:
        data = data_socket.recv(1024)
        print(f"Chunk received: {data}")  # Debug print

        if b'END' in data:
            file_data_part, checksum_part = data.split(b'END', 1)
            file_data.extend(file_data_part)
            received_checksum = checksum_part.decode().strip()
            break
        elif not data:
            print("No more data received. Exiting loop.")
            break
        else:
            file_data.extend(data)

    with open(filename, 'wb') as file:
        file.write(file_data)
    print(f"File reception completed for: {filename}")

    # Checksum verification
    client_checksum = calculate_file_hash(filename)
    print(f"Checksum for received file: {client_checksum}")
    if client_checksum == received_checksum:
        print("Checksum verified. File received successfully.")
    else:
        print("Checksum mismatch. File might be corrupted.")
    
    print(f"Completed receiving {filename}, {len(file_data)} bytes transferred.")

def send_file(data_socket, command):
    filename = command.split()[1]
    total_bytes_sent = 0

    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            total_bytes_sent = len(file_data)
            file_hash = hashlib.md5(file_data).hexdigest()
            print(f"Checksum for file to send: {file_hash}")

            # Sending file data
            data_socket.sendall(file_data)
            data_socket.send(b'END')
            # Sending checksum
            data_socket.sendall(file_hash.encode())

        print(f"Completed sending file {filename}, {total_bytes_sent} bytes transferred")
    except FileNotFoundError:
        print("File not found.")


def handle_other_commands(client_socket):
    response = b""
    while True:
        part = client_socket.recv(1024)
        response += part
        if b"END_OF_LS" in part:
            print(response.decode().replace("END_OF_LS", ""))
            break

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to server.")

        while True:
            command = input("ftp> ").strip()
            if not command:
                continue

            if command.lower().startswith(('get ', 'put ')):
                handle_file_transfer(client_socket, command)
            elif command.lower() == 'quit':
                break
            else:
                client_socket.send(command.encode())
                handle_other_commands(client_socket)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
    else:
        server_ip = 'localhost'
        server_port = 21

    start_client(server_ip, server_port)
