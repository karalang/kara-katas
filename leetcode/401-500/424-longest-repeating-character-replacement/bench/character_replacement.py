# Benchmark for #424: mirror of character_replacement.kara (a window that
# never shrinks).
import sys


def character_replacement(s, k):
    count = [0] * 26
    best = 0
    left = 0
    for right in range(len(s)):
        c = ord(s[right]) - 65
        count[c] += 1
        best = max(best, count[c])
        if right - left + 1 - best > k:
            count[ord(s[left]) - 65] -= 1
            left += 1
    return len(s) - left


seed = 424


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


calls = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
size = 1000000
parts = []
length_so_far = 0
while length_so_far < size:
    letter = chr(65 + step() % 5)
    run = 1 + step() % 8
    take = min(run, size - length_so_far)
    parts.append(letter * take)
    length_so_far += take
text = "".join(parts)
total = 0
checksum = 0
for _ in range(calls):
    length = 10000 + step() * 3 % 90000
    start = step() * 30 % (size - length)
    k = step() % 50
    answer = character_replacement(text[start:start + length], k)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"{calls} calls: total {total}, checksum {checksum}")
