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
    data += ' ' * (16 - len(data) % 16)
    matrix = [list(data[i:i+4]) for i in range(0, len(data), 4)]
    row_par = [str(sum(ord(c) % 2 for c in row) % 2) for row in matrix]
    col_par = []
    for c in range(4):
        col_par.append(str(sum(ord(matrix[r][c]) % 2 for r in range(len(matrix))) % 2))
    return ''.join(row_par + col_par)

def compute_hamming(data):
    result = ''
    for c in data:
        bits = format(ord(c), '08b')
        for i in range(0, 8, 4):
            d = [int(b) for b in bits[i:i+4]]
            if len(d) < 4: d += [0]*(4-len(d))
            p1 = d[0] ^ d[1] ^ d[3]
            p2 = d[0] ^ d[2] ^ d[3]
            p3 = d[1] ^ d[2] ^ d[3]
            code = [p1, p2, d[0], p3, d[1], d[2], d[3]]
            result += ''.join(map(str, code))
    return result

methods = {
    '1': ('PARITY_EVEN', lambda d: compute_parity(d, 'even')),
    '2': ('PARITY_ODD', lambda d: compute_parity(d, 'odd')),
    '3': ('2D_PARITY', compute_2d_parity),
    '4': ('CRC16', compute_crc16),
    '5': ('HAMMING', compute_hamming),
    '6': ('CHECKSUM', compute_checksum),
}

print("Client 1 - Gönderici")
text = input("Metin gir: ")
print("\nYöntemler:")
for k, v in methods.items(): print(f"{k}: {v[0]}")
choice = input("Seçim (1-6): ")

method_name, control_func = methods[choice]
control = control_func(text)
packet = f"{text}|{method_name}|{control}"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5000))
s.send(packet.encode('utf-8'))
print(f"Gönderilen: {packet}")
s.close()