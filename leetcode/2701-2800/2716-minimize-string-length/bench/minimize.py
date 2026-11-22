# LeetCode #2716: Minimize String Length -- the bench (minimize.kara in
# Python): the distinct letters of each string counted by a set.


def minimized_string_length(s):
    return len(set(s))


seed = 2716


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds = 100000, 10
strings = []
for _ in range(count):
    letters = next_random() % 26 + 1
    strings.append("".join(chr(ord("a") + next_random() % letters) for _ in range(100)))
total = 0
check = 0
for r in range(rounds):
    for s in strings:
        length = minimized_string_length(s)
        total += length
        check = (check * 31 + length + r) % 1000000007
print(f"{count} strings of 100 letters, {rounds} rounds: lengths sum to {total}, checksum {check}")
