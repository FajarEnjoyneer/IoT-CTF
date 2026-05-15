import socket
import struct
import threading
import time

SERVER_HOST = "20.18.149.51"
SERVER_PORT = 13337

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
    # data must be up to 8 bytes
    dlc = len(data)
    # struct can_frame: can_id (4), dlc (1), pad (1), res0 (1), res1 (1), data (8)
    frame = struct.pack("<IBBBB8s", can_id, dlc, 0, 0, 0, data.ljust(8, b"\x00"))
    sock.sendall(struct.pack(">H", len(frame)) + frame)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

    sock.sendall(struct.pack(">H", 0) + b"\x01") # PING
    
    def receive_loop():
        full_data = b""
        try:
            while True:
                header = recv_exact(sock, 2)
                frame_len = struct.unpack(">H", header)[0]
                if frame_len == 0:
                    control_type = recv_exact(sock, 1)[0]
                    if control_type == 1:
                        sock.sendall(struct.pack(">H", 0) + b"\x02")
                    continue
                
                frame = recv_exact(sock, frame_len)
                can_id = struct.unpack("<I", frame[:4])[0]
                can_dlc = frame[4]
                can_data = frame[8:8+8]
                
                if can_id == 0x7e8:
                    pci = can_data[0]
                    if (pci & 0xF0) == 0x00: # Single Frame
                        length = pci & 0x0F
                        payload = can_data[1:1+length]
                        print(f"SF Payload: {payload.hex(' ')} | ASCII: {''.join(chr(b) if 0x20<=b<=0x7e else '.' for b in payload)}")
                    
                    elif (pci & 0xF0) == 0x10: # First Frame
                        length = ((pci & 0x0F) << 8) | can_data[1]
                        payload = can_data[2:]
                        full_data = payload
                        print(f"FF total_len={length}, data: {payload.hex(' ')}")
                        # Send Flow Control
                        send_can(sock, 0x7e0, b"\x30\x00\x00\x00\x00\x00\x00\x00")
                    
                    elif (pci & 0xF0) == 0x20: # Consecutive Frame
                        payload = can_data[1:]
                        full_data += payload
                        print(f"CF data: {payload.hex(' ')}")
                        if b"}" in full_data:
                            print(f"\n--- RECONSTRUCTED DATA ---")
                            ascii_res = "".join(chr(b) if 0x20<=b<=0x7e else "." for b in full_data)
                            print(f"RAW: {full_data.hex(' ')}")
                            print(f"STR: {ascii_res}")
        except Exception as e:
            print(f"Error: {e}")

    threading.Thread(target=receive_loop, daemon=True).start()

    time.sleep(1)
    send_can(sock, 0x7e0, b"\x02\x3e\x80\x00\x00\x00\x00\x00")
    time.sleep(0.5)

    # Request VIN (F1 90)
    print("Requesting VIN (0xF190)...")
    send_can(sock, 0x7e0, b"\x03\x22\xf1\x90\x00\x00\x00\x00")
    
    time.sleep(2)
    
    # Request other DIDs just in case
    print("Requesting 0xF191...")
    send_can(sock, 0x7e0, b"\x03\x22\xf1\x91\x00\x00\x00\x00")
    
    time.sleep(5)

if __name__ == "__main__":
    main()
