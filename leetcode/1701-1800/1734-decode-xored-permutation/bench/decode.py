# LeetCode #1734: Decode XORed Permutation -- the bench (decode.kara): the
# first value from the XOR of 1 to n less that of the codes at odd places,
# then each next value the last XORed with its code.


def decode(encoded):
    n = len(encoded) + 1
    all_ = 0
    for v in range(1, n + 1):
        all_ ^= v
    rest = 0
    i = 1
    while i < n - 1:
        rest ^= encoded[i]
        i += 2
    perm = [all_ ^ rest]
    for code in encoded:
        perm.append(perm[-1] ^ code)
    return perm


seed = 1734


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


count = 50
rounds = 40
n = 99999
problems = []
for _ in range(count):
    perm = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = wide() % (i + 1)
        perm[i], perm[j] = perm[j], perm[i]
    problems.append([perm[i] ^ perm[i + 1] for i in range(n - 1)])
total = 0
check = 0
for r in range(rounds):
    for encoded in problems:
        perm = decode(encoded)
        total += perm[0]
        check = (check * 31 + perm[0] + perm[n // 2] + perm[n - 1] + r) % 1000000007
print(f"{count} permutations of {n}, {rounds} rounds: first values sum to {total}, checksum {check}")
