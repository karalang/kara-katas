# LeetCode #1720: Decode XORed Array -- the bench (decode.kara): each
# value the one before it XORed with the code between them.


def decode(encoded, first):
    arr = [first]
    for e in encoded:
        arr.append(arr[-1] ^ e)
    return arr


seed = 1720


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    count = 200
    rounds = 100
    n = 10000
    problems = []
    for _ in range(count):
        encoded = [wide() % 100001 for _ in range(n)]
        first = wide() % 100001
        problems.append((encoded, first))
    total = 0
    check = 0
    for r in range(rounds):
        for encoded, first in problems:
            arr = decode(encoded, first)
            total += arr[n]
            check = (check * 31 + arr[n // 2] + arr[n] + r) % 1000000007
    print(f"{count} arrays of {n} codes, {rounds} rounds: last values sum to {total}, checksum {check}")


main()
