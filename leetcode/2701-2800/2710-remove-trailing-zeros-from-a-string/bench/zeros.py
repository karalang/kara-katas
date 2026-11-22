# LeetCode #2710: Remove Trailing Zeros From a String -- the bench
# (zeros.kara in Python): an index walks back over the zeros, and the
# digits before it are copied out.


def remove_trailing_zeros(num):
    end = len(num)
    while num[end - 1] == "0":
        end -= 1
    return num[:end]


seed = 2710


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds = 20000, 20
numbers = []
for _ in range(count):
    zeros = next_random() % 1000
    digits = [chr(ord("1") + next_random() % 9)]
    for _ in range(1, 1000 - zeros):
        digits.append(chr(ord("0") + next_random() % 10))
    numbers.append("".join(digits) + "0" * zeros)
total = 0
check = 0
for r in range(rounds):
    for num in numbers:
        out = remove_trailing_zeros(num)
        kept = len(out)
        total += kept
        check = (check * 31 + kept + ord(out[kept - 1]) + r) % 1000000007
print(f"{count} numbers of 1000 digits, {rounds} rounds: {total} digits kept, checksum {check}")
