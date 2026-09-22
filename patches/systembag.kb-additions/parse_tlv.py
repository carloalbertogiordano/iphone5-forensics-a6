import struct, sys, binascii

def parse_tlv(data):
    pos = 0
    while pos + 8 <= len(data):
        tag = data[pos:pos+4].decode('ascii', errors='replace')
        length = struct.unpack('>I', data[pos+4:pos+8])[0]
        value = data[pos+8:pos+8+length]
        yield tag, length, value
        pos += 8 + length

with open(sys.argv[1], 'rb') as f:
    outer = f.read()

# primo livello: DATA + SIGN
for tag, length, value in parse_tlv(outer):
    if tag == 'DATA':
        print("=== KEYBAG HEADER ===")
        current_uuid = None
        current_class = None
        for t, l, v in parse_tlv(value):
            if t == 'UUID':
                if current_uuid and current_class:
                    print()
                current_uuid = binascii.hexlify(v).decode()
                current_class = None
                print(f"--- KEY ---")
                print(f"  UUID: {current_uuid}")
            elif t == 'CLAS':
                current_class = struct.unpack('>I', v)[0]
                print(f"  CLAS: {current_class}")
            elif t == 'WRAP':
                print(f"  WRAP: {struct.unpack('>I', v)[0]}")
            elif t == 'WPKY':
                print(f"  WPKY: {binascii.hexlify(v).decode()}")
            elif t == 'KTYP':
                print(f"  KTYP: {struct.unpack('>I', v)[0]}")
            else:
                if l <= 8:
                    print(f"{t}: {struct.unpack('>I', v[:4])[0] if l==4 else binascii.hexlify(v).decode()}")
                else:
                    print(f"{t}: {binascii.hexlify(v).decode()}")
    elif tag == 'SIGN':
        print(f"\nSIGN: {binascii.hexlify(value).decode()}")
