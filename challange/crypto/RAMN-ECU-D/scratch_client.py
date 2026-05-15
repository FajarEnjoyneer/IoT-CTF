import socket
import struct
import threading
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
                print(f"CAN ID: {can_id:03x} DLC: {can_dlc} Data: {data.hex(' ')}")
        except Exception as e:
            print(f"Error: {e}")

    threading.Thread(target=receive_loop, daemon=True).start()

    # Wait a bit to see if anything comes in
    time.sleep(5)
    
    # Try to send a UDS request: Service 10 03 (Diagnostic Session Control: Extended)
    # CAN ID 7e0, DLC 8, Data: 02 10 03 00 00 00 00 00 (ISO-TP Single Frame)
    def send_can(can_id, data):
        # struct can_frame { can_id_t can_id; __u8 can_dlc; __u8 __pad; __u8 __res0; __u8 __res1; __u8 data[8]; }
        # can_id is 4 bytes, dlc 1, pad 1, res0 1, res1 1, data 8 = 16 bytes
        frame = struct.pack("<IBBBB8s", can_id, len(data), 0, 0, 0, data.ljust(8, b"\x00"))
        sock.sendall(struct.pack(">H", len(frame)) + frame)

    print("Sending UDS DiagnosticSessionControl (Extended)...")
    send_can(0x7e0, b"\x02\x10\x03\x00\x00\x00\x00\x00")
    
    time.sleep(2)
    
    # Try to read a DID: e.g., F1 90 (VIN)
    print("Sending UDS ReadDataByIdentifier (VIN - 0xF190)...")
    send_can(0x7e0, b"\x03\x22\xf1\x90\x00\x00\x00\x00")

    time.sleep(5)

if __name__ == "__main__":
    main()
