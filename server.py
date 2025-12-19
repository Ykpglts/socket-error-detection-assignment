import socket
import random

def corrupt(data):
    if random.random() < 0.7:  # 
        choice = random.randint(1, 5)
        if choice == 1:  # 
            pos = random.randint(0, len(data)-1)
            return data[:pos] + chr(ord(data[pos]) ^ 1) + data[pos+1:]
        elif choice == 2:  # 
            pos = random.randint(0, len(data)-1)
            return data[:pos] + chr(random.randint(32,126)) + data[pos+1:]
        elif choice == 3:  # sil
            pos = random.randint(0, len(data)-1)
            return data[:pos] + data[pos+1:]
        elif choice == 4:  # ekle
            pos = random.randint(0, len(data))
            return data[:pos] + chr(random.randint(32,126)) + data[pos:]
        elif choice == 5:  # swap
            pos = random.randint(0, len(data)-2)
            return data[:pos] + data[pos+1] + data[pos] + data[pos+2:]
    return data

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5000))
server.listen()

print("Server çalışıyor...")

conn, addr = server.accept()
packet = conn.recv(1024).decode('utf-8')
print(f"Client1'den alınan: {packet}")

data, method, control = packet.split('|', 2)
corrupted_data = corrupt(data)
new_packet = f"{corrupted_data}|{method}|{control}"

client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(('127.0.0.1', 5001))
client2.send(new_packet.encode('utf-8'))
print(f"Client2'ye gönderilen: {new_packet}")

client2.close()
conn.close()