# Benchmark for #600: Python mirror of the ★ arm (walk the bits with
# Fibonacci counts); see find_integers.kara.


def find_integers(n):
    fib = [1, 2]
    for k in range(2, 32):
        fib.append(fib[k - 1] + fib[k - 2])
    count = 0
    previous = False
    for k in range(31, -1, -1):
        if (n >> k) & 1 == 1:
            count += fib[k]
            if previous:
                return count
            previous = True
        else:
            previous = False
    return count + 1


# ---- benchmark ----------------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 1000000
    rounds = 20
    seed = [600]
    values = []
    for _ in range(count):
        hi = step(seed)
        lo = step(seed)
        values.append(1 + (hi * 32768 + lo) % 1000000000)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            got = find_integers(values[(rnd * 7 + g) % count])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} values, {rounds} rounds: total {total}, checksum {checksum}")


main()
