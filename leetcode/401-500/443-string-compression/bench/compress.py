# Benchmark for #443: mirror of compress.kara (reading and writing in
# place) on 1,000 random strings of 2,000 characters, built once, copied
# and compressed 20 times over.


def compress(chars):
    n = len(chars)
    read = 0
    write = 0
    while read < n:
        c = chars[read]
        start = read
        while read < n and chars[read] == c:
            read += 1
        chars[write] = c
        write += 1
        count = read - start
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1
    return write


seed = 443


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 1000, 2000, 20
    # Runs of 1 to 1, 3, 15 or 120 letters from a three-letter alphabet.
    strings = []
    for _ in range(count):
        longest = [1, 3, 15, 120][next_random() % 4]
        chars = []
        while len(chars) < size:
            c = chr(97 + next_random() % 3)
            run = 1 + next_random() % longest
            for _ in range(run):
                if len(chars) < size:
                    chars.append(c)
        strings.append(chars)
    length = 0
    checksum = 0
    for round in range(rounds):
        for i in range(count):
            chars = list(strings[i])
            n = compress(chars)
            length += n
            checksum = (checksum * 31 + n + ord(chars[n - 1]) + round) % 1000000007
    print(f"{rounds} rounds on {count} strings of {size}: compressed length {length}, checksum {checksum}")


main()
