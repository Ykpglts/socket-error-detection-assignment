import socket

def compute_parity(data, parity_type='even'):
    count = sum(bin(ord(c)).count('1') for c in data)
    if parity_type == 'even':
        p = 0 if count % 2 == 0 else 1
    else:
        p = 1 if count % 2 == 0 else 0
    return f"{p}"

def compute_crc16(data):
    crc = 0xFFFF
    poly = 0x1021
    for byte in data.encode('ascii'):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF
    return f"{crc:04X}"

def compute_checksum(data):
    s = 0
    for i in range(0, len(data), 2):
        if i+1 < len(data):
            w = (ord(data[i]) << 8) + ord(data[i+1])
        else:
            w = ord(data[i]) << 8
        s += w
    s = (s >> 16) + (s & 0xFFFF)
    s = s + (s >> 16)
    return f"{(~s & 0xFFFF):04X}"

def compute_2d_parity(data):
    # 16 karaktere tamamla (4x4 matris)
    data += ' ' * (16 - len(data) % 16)
    matrix = [list(data[i:i+4]) for i in range(0, len(data), 4)]
    row_par = []
    for row in matrix:
        p = sum(ord(c) % 2 for c in row) % 2
        row_par.append(str(p))
    col_par = []
    for c in range(4):
        p = sum(ord(matrix[r][c]) % 2 for r in range(4)) % 2
        col_par.append(str(p))
    return ''.join(row_par + col_par)

def compute_hamming(data):
    result = ''
    for c in data:
        bits = format(ord(c), '08b')
        for i in range(0, 8, 4):
            d = [int(b) for b in bits[i:i+4]]
            if len(d) < 4: d += [0] * (4 - len(d))
            p1 = d[0] ^ d[1] ^ d[3]
            p2 = d[0] ^ d[2] ^ d[3]
            p3 = d[1] ^ d[2] ^ d[3]
            code = [p1, p2, d[0], p3, d[1], d[2], d[3]]
            result += ''.join(map(str, code))
    return result

# Ana kısım
print("Client2 (Alıcı) çalışıyor, server'dan bekliyor...")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5001))
server.listen(1)

conn, addr = server.accept()
packet = conn.recv(1024).decode('utf-8')
print(f"Alınan paket: {packet}")

data, method, received_control = packet.split('|', 2)

# Kontrol hesapla
if 'PARITY' in method:
    expected = compute_parity(data, 'even' if 'EVEN' in method else 'odd')
elif method == 'CRC16':
    expected = compute_crc16(data)
elif method == 'CHECKSUM':
    expected = compute_checksum(data)
elif method == '2D_PARITY':
    expected = compute_2d_parity(data)
elif method == 'HAMMING':
    expected = compute_hamming(data)
else:
    expected = "BİLİNMEYEN YÖNTEM"

if expected == received_control:
    print("Hata YOK! Veri doğru geldi.")
    print(f"Alınan veri: {data}")
else:
    print("HATA TESPİT EDİLDİ!")
    print(f"Beklenen control: {expected}")
    print(f"Alınan control : {received_control}")
    print(f"Alınan (muhtemelen bozulmuş) veri: {data}")

conn.close()
server.close()