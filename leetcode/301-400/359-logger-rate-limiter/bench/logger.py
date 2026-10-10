# Benchmark for #359 -- mirror of logger.kara.


def main():
    next_ok = {}
    seed = 359
    t = 0
    printed = 0
    checksum = 0
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        t += 1 if (seed // 65536) % 8 == 0 else 0
        seed = (seed * 1103515245 + 12345) % 2147483648
        message = f"msg{(seed // 65536) % 100}"
        prev = next_ok.get(message)
        ok = prev is None or t >= prev
        if ok:
            next_ok[message] = t + 10
            printed += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"{printed} of 1000000 calls printed, checksum {checksum}")


main()
