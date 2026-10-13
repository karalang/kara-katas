# Benchmark for #466: mirror of count_repetitions.kara (the star arm: find
# the cycle) on the same workload.


def get_max_repetitions(s1, n1, s2, n2):
    a = list(s1)
    b = list(s2)
    index = 0
    count = 0
    seen = {}
    k = 0
    while k < n1:
        for c in a:
            if c == b[index]:
                index += 1
                if index == len(b):
                    index = 0
                    count += 1
        k += 1
        if index in seen:
            k0, count0 = seen[index]
            cycle = k - k0
            cycles = (n1 - k) // cycle
            count += cycles * (count - count0)
            k += cycles * cycle
            while k < n1:
                for c in a:
                    if c == b[index]:
                        index += 1
                        if index == len(b):
                            index = 0
                            count += 1
                k += 1
            break
        seen[index] = (k, count)
    return count // n2


def main():
    pairs = 100
    rounds = 1000
    seed = 466

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    firsts = []
    seconds = []
    for _ in range(pairs):
        s1 = "".join(chr(97 + next_random() % 26) for _ in range(100))
        s2 = "".join(s1[next_random() % 100] for _ in range(1 + next_random() % 100))
        firsts.append(s1)
        seconds.append(s2)
    total = 0
    checksum = 0
    for _ in range(rounds):
        for p in range(pairs):
            hi = next_random()
            lo = next_random()
            n1 = 1 + (hi * 32768 + lo) % 1000000
            n2 = 1 + next_random() % 100
            m = get_max_repetitions(firsts[p], n1, seconds[p], n2)
            total += m
            checksum = (checksum * 31 + m) % 1000000007
    print(f"{rounds} rounds on {pairs} pairs: {total} repetitions in all, checksum {checksum}")


main()
