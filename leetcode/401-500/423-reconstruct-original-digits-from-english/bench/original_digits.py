# Benchmark for #423: mirror of original_digits.kara (unique letters).
import sys


def original_digits(s):
    letters = [0] * 26
    for ch in s:
        letters[ord(ch) - 97] += 1

    def at(c):
        return letters[ord(c) - 97]

    count = [0] * 10
    count[0] = at("z")
    count[2] = at("w")
    count[4] = at("u")
    count[6] = at("x")
    count[8] = at("g")
    count[3] = at("h") - count[8]
    count[5] = at("f") - count[4]
    count[7] = at("s") - count[6]
    count[1] = at("o") - count[0] - count[2] - count[4]
    count[9] = at("i") - count[5] - count[6] - count[8]
    return "".join(str(d) * count[d] for d in range(10))


seed = 423


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


calls = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
blocks = 20000
names = "zero one two three four five six seven eight nine".split()
parts = []
ends = [0]
length_so_far = 0
for _ in range(blocks):
    count = 1 + step() % 8
    pool = []
    for _ in range(count):
        pool.extend(names[step() % 10])
    for i in range(len(pool)):
        j = i + step() % (len(pool) - i)
        pool[i], pool[j] = pool[j], pool[i]
    parts.append("".join(pool))
    length_so_far += len(pool)
    ends.append(length_so_far)
text = "".join(parts)
digits = 0
checksum = 0
for _ in range(calls):
    length = 50 + step() % 200
    first = step() % (blocks - length)
    answer = original_digits(text[ends[first]:ends[first + length]])
    digits += len(answer)
    for ch in answer:
        checksum = (checksum * 31 + (ord(ch) - 47)) % 1000000007
print(f"{calls} calls on {len(text)} letters: {digits} digits, checksum {checksum}")
