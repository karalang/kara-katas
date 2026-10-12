# Benchmark mirror of ransom_note.kara (#383).


def can_construct(ransom_note, magazine):
    count = [0] * 26
    for b in magazine:
        count[b - 97] += 1
    for b in ransom_note:
        count[b - 97] -= 1
        if count[b - 97] < 0:
            return False
    return True


def main():
    seed = 383
    pool = bytearray()
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append((seed // 65536) % 26 + 97)
    pool = bytes(pool)
    yes = 0
    checksum = 0
    for _ in range(10000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 30000 + (seed // 64) % 40000
        seed = (seed * 1103515245 + 12345) % 2147483648
        m = 40000 + (seed // 64) % 40000
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = (seed // 64) % (1000000 - n)
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = (seed // 64) % (1000000 - m)
        ok = can_construct(memoryview(pool)[a:a + n], memoryview(pool)[b:b + m])
        if ok:
            yes += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"{yes} of 10000 can be built, checksum {checksum}")


main()
