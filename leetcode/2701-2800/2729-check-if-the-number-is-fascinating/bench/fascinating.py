# LeetCode #2729: Check if The Number is Fascinating -- the bench
# (fascinating.kara in Python): n, 2 n and 3 n joined by an f-string, the
# digits sorted and compared with "123456789".


def is_fascinating(n):
    return "".join(sorted(f"{n}{2 * n}{3 * n}")) == "123456789"


seed = 2729


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds = 1000000, 5
fascinating = [192, 219, 273, 327]
numbers = []
for i in range(count):
    if i % 50 == 0:
        numbers.append(fascinating[next_random() % 4])
    else:
        numbers.append(next_random() % 900 + 100)
yes = 0
check = 0
for r in range(rounds):
    for n in numbers:
        answer = is_fascinating(n)
        if answer:
            yes += 1
        check = (check * 31 + (2 if answer else 1) + r) % 1000000007
print(f"{count} numbers, {rounds} rounds: {yes} fascinating, checksum {check}")
