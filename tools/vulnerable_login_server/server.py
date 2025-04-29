import socket
import threading
import hashlib

HOST = "127.0.0.1"
PORT = 9090

users = {
    "admin": hashlib.md5("password123".encode()).hexdigest()
}

def handle_client(conn, addr):
    conn.sendall(b"== Welcome to SecureCorp Login ==")
    conn.sendall(b"\nUsername: ")
    username = conn.recv(1024).decode().strip()

    conn.sendall(b"Password: ")
    password = conn.recv(1024).decode().strip()

    hashed = hashlib.md5(password.encode()).hexdigest()

    if username in users and users[username] == hashed:
        conn.sendall(b"\nLogin successful!\n")
        with open("flag.txt", "rb") as f:
            conn.sendall(b"FLAG: " + f.read() + b"\n")
    else:
        conn.sendall(b"\nAccess denied.\n")
    
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}...")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
