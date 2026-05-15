import socket
import struct
import threading
import time

SERVER_HOST = "20.18.149.51"
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

def send_can(sock, can_id, data):
    # struct can_frame { can_id_t can_id; __u8 can_dlc; __u8 __pad; __u8 __res0; __u8 __res1; __u8 data[8]; }
    frame = struct.pack("<IBBBB8s", can_id, len(data), 0, 0, 0, data.ljust(8, b"\x00"))
    sock.sendall(struct.pack(">H", len(frame)) + frame)
    print(f"SENT CAN ID: {can_id:03x} Data: {data.hex(' ')}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

    # Send PING
    sock.sendall(struct.pack(">H", 0) + b"\x01")
    
    def receive_loop():
        try:
            while True:
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
                
                # Only print interesting IDs (UDS response or anything else that looks like a flag)
                if can_id == 0x7e8:
                    print(f"RECV CAN ID: {can_id:03x} Data: {data.hex(' ')}")
                elif b"FLAG" in data or b"flag" in data:
                    print(f"!!! FLAG DETECTED !!! CAN ID: {can_id:03x} Data: {data.hex(' ')}")
        except Exception as e:
            print(f"Error: {e}")

    threading.Thread(target=receive_loop, daemon=True).start()

    time.sleep(1)
    
    # 1. Tester Present
    send_can(sock, 0x7e0, b"\x02\x3e\x80\x00\x00\x00\x00\x00")
    time.sleep(0.5)

    # 2. Read VIN (DID 0xF190)
    send_can(sock, 0x7e0, b"\x03\x22\xf1\x90\x00\x00\x00\x00")
    
    time.sleep(2)
    
    # 3. Try Session 03
    send_can(sock, 0x7e0, b"\x02\x10\x03\x00\x00\x00\x00\x00")
    time.sleep(0.5)
    
    # 4. Try Session 02 (Programming)
    send_can(sock, 0x7e0, b"\x02\x10\x02\x00\x00\x00\x00\x00")
    time.sleep(0.5)

    # 5. Scan common DIDs
    common_dids = [0xF190, 0xF181, 0xF187, 0xF189, 0xF191, 0xF19E]
    for did in common_dids:
        print(f"Scanning DID 0x{did:04x}...")
        did_high = (did >> 8) & 0xFF
        did_low = did & 0xFF
        send_can(sock, 0x7e0, struct.pack("BBBBBBBB", 0x03, 0x22, did_high, did_low, 0, 0, 0, 0))
        time.sleep(0.5)

    time.sleep(5)

if __name__ == "__main__":
    main()
