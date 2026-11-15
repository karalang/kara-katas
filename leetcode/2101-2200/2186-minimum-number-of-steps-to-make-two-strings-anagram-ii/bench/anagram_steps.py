# LeetCode #2186: Minimum Number of Steps to Make Two Strings Anagram II
# -- the benchmark's Python mirror of anagram_steps.kara: one balance of
# 26 counts.


def min_steps(s, t):
    balance = [0] * 26
    for b in s.encode():
        balance[b - 97] += 1
    for b in t.encode():
        balance[b - 97] -= 1
    steps = 0
    for d in balance:
        steps += abs(d)
    return steps


seed = 2186


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = "".join(chr(97 + next_random() % 26) for _ in range(1000000))
    check = 0
    for _ in range(200):
        a = next_random()
        b = next_random()
        c = next_random()
        d = next_random()
        i = (a * 32768 + b) % 800001
        j = (c * 32768 + d) % 800001
        steps = min_steps(row[i:i + 200000], row[j:j + 200000])
        check = (check * 31 + steps) % 1000000007
    print(f"200 solves: checksum {check}")


main()
