# Benchmark for #555: Python mirror of the ★ arm (every cut, the rest at
# its best); see split_concatenated_strings.kara.

seed = 555


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def split_loop(strs):
    n = len(strs)
    larger = []
    for s in strs:
        r = s[::-1]
        larger.append(r if r > s else s)
    answer = ""
    for i in range(n):
        middle = "".join(larger[(i + j) % n] for j in range(1, n))
        for t in (strs[i], strs[i][::-1]):
            for k in range(len(t)):
                candidate = t[k:] + middle + t[:k]
                if candidate > answer:
                    answer = candidate
    return answer


def main():
    count = 100
    lists = []
    strings = 0
    for _ in range(count):
        alphabet = 2 + next_random() % 25
        strs = []
        left = 1000
        while left > 0:
            length = min(1 + next_random() % 40, left)
            strs.append("".join(chr(97 + next_random() % alphabet) for _ in range(length)))
            left -= length
        strings += len(strs)
        lists.append(strs)
    checksum = 0
    for rnd in range(30):
        for g in range(count):
            b = split_loop(lists[(rnd * 7 + g) % count]).encode()
            checksum = (checksum * 31 + len(b) + b[0] * 7 + b[len(b) // 2]) % 1000000007
    print(f"{count} lists, {strings} strings, 30 rounds each: checksum {checksum}")


main()
