# Python mirror of the utf8-codepoints decode bench — same algorithm, same sink.
MODULUS = 1000000007
REPEAT = 9523
ITERS = 400

def utf8_byte_len(lead):
    if lead < 0x80: return 1
    elif 0xC0 <= lead <= 0xDF: return 2
    elif 0xE0 <= lead <= 0xEF: return 3
    elif 0xF0 <= lead <= 0xF7: return 4
    else: return 1

def main():
    cps = [0x61,0x62,0x63,0x20,0x31,0x32,0x33,0x20,
           0xe9,0xf1,0x3b1,0x3b2,0x434,0x436,
           0x65e5,0x672c,0x1d11e,0x1f980,0x20]
    base = "".join(chr(c) for c in cps)
    buf = (base * REPEAT).encode("utf-8")
    n = len(buf)
    sink = 0
    count = 0
    for _ in range(ITERS):
        i = 0
        while i < n:
            lead = buf[i]
            ln = utf8_byte_len(lead)
            if ln == 1: cp = lead
            elif ln == 2: cp = lead & 0x1F
            elif ln == 3: cp = lead & 0x0F
            else: cp = lead & 0x07
            k = 1
            while k < ln and i + k < n:
                cp = (cp << 6) | (buf[i + k] & 0x3F)
                k += 1
            sink = (sink + cp) % MODULUS
            count += 1
            i += ln
    print(f"{count} {sink}")

main()
