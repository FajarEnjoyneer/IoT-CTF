import socket
import struct
import time

SERVER_HOST = "20.210.80.68"
SERVER_PORT = 13337

CAN_MTU = 16
FRAME_HEADER_SIZE = 2

def recv_exact(sock, size):
    chunks = []
    remaining = size
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise EOFError("peer closed the TCP connection")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

    # Send PING
    sock.sendall(struct.pack(">H", 0) + b"\x01")
    
    start_time = time.time()
    try:
        sock.settimeout(5.0)
        while time.time() - start_time < 30:
            try:
                header = recv_exact(sock, FRAME_HEADER_SIZE)
                frame_len = struct.unpack(">H", header)[0]
                if frame_len == 0:
                    control_type = recv_exact(sock, 1)[0]
                    if control_type == 1: # PING
                        sock.sendall(struct.pack(">H", 0) + b"\x02") # PONG
                    continue
                
                frame = recv_exact(sock, frame_len)
                can_id = struct.unpack("<I", frame[:4])[0]
                can_dlc = frame[8]
                data = frame[12:12+can_dlc]
                print(f"[{time.time()-start_time:.2f}] CAN ID: {can_id:03x} DLC: {can_dlc} Data: {data.hex(' ')}")
            except socket.timeout:
                # Send PING to keep alive
                sock.sendall(struct.pack(">H", 0) + b"\x01")
                continue
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
