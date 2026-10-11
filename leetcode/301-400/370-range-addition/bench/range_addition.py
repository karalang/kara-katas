# Benchmark for #370 -- mirror of range_addition.kara.


def get_modified_array(length, updates):
    diff = [0] * (length + 1)
    for start, end, inc in updates:
        diff[start] += inc
        diff[end + 1] -= inc
    out = [0] * length
    running = 0
    for i in range(length):
        running += diff[i]
        out[i] = running
    return out


def main():
    seed = 370
    checksum = 0
    for _ in range(50):
        updates = []
        for _ in range(10000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            high = seed // 65536
            seed = (seed * 1103515245 + 12345) % 2147483648
            a = (high * 32768 + seed // 65536) % 100000
            seed = (seed * 1103515245 + 12345) % 2147483648
            high2 = seed // 65536
            seed = (seed * 1103515245 + 12345) % 2147483648
            b = (high2 * 32768 + seed // 65536) % 100000
            seed = (seed * 1103515245 + 12345) % 2147483648
            inc = (seed // 65536) % 2001 - 1000
            updates.append((min(a, b), max(a, b), inc))
        out = get_modified_array(100000, updates)
        for v in out:
            checksum = (checksum * 31 + v + 100000000) % 1000000007
    print(f"checksum {checksum}")


main()
