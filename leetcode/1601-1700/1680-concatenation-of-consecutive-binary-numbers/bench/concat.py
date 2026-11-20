# LeetCode #1680: Concatenation of Consecutive Binary Numbers -- the bench's
# Python mirror: the ★ arm on 800 random n up to 100000, all drawn first,
# each answered 5 times.


def concatenated_binary(n):
    modulus = 1000000007
    value = 0
    bits = 0
    for i in range(1, n + 1):
        if i & (i - 1) == 0:
            bits += 1
        value = ((value << bits) + i) % modulus
    return value


seed = 1680


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 800, 5
    ns = [(next_random() * 32768 + next_random()) % 100000 + 1 for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for n in ns:
            answer = concatenated_binary(n)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} values of n, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
