import struct
import sys

def do_patch1(data):
    occurrences = data.split(struct.pack('<L', 0x8082f000))
    output = occurrences[0]
    for i, occurrence in enumerate(occurrences[1:]):
        noop = struct.pack('<L', 0x0135f640)
        output += noop + occurrence
    return output

def do_patch2(data):
    occurrences = data.split(struct.pack('<L', 0xff77f003))
    output = occurrences[0]
    for i, occurrence in enumerate(occurrences[1:]):
        noop = struct.pack('<L', 0x20402040)
        output += noop + occurrence
    return output

def do_patch3(data):
    occurrences = data.split(struct.pack('<L', 0x68bad370))
    output = occurrences[0]
    for i, occurrence in enumerate(occurrences[1:]):
        noop = struct.pack('<L', 0x68ba2864)
        output += noop + occurrence
    return output

def main():
    infile, offset_hex, length_hex, outfile = sys.argv[1:]
    offset = int(offset_hex, base=16)
    length = int(length_hex, base=16)
    with open(infile, "rb") as inf:
        data = inf.read()
        with open(outfile, "wb") as ouf:
            patched = do_patch3(do_patch2(do_patch1(data[offset:offset + length])))
            ouf.write(data[:offset] + patched + data[offset + length:])

if __name__ == "__main__":
    main()
