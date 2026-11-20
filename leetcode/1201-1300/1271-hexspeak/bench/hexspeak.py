# LeetCode #1271 bench, in Python: the ★ arm (the decimal text parsed, its
# hexadecimal digits spelled from the lowest, 0 as O, 1 as I, 10 to 15 as A
# to F, any other an error) on 100,000 numbers up to 10^12 drawn once, half
# spelled in the eight letters, 150 rounds; every answer folded into a
# checksum.


def to_hexspeak(num):
    n = int(num)
    letters = []
    while n > 0:
        d = n % 16
        if d == 0:
            letters.append("O")
        elif d == 1:
            letters.append("I")
        elif d >= 10:
            letters.append(chr(ord("A") + d - 10))
        else:
            return "ERROR"
        n //= 16
    return "".join(reversed(letters))


seed = 1271


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


letters = [0, 1, 10, 11, 12, 13, 14, 15]
nums = []
for i in range(100000):
    if i % 2 == 0:
        a = next_random()
        b = next_random()
        n = (a * 32768 + b) % 1000000000000 + 1
    else:
        n = 1
        for _ in range(next_random() % 9):
            n = n * 16 + letters[next_random() % 8]
    nums.append(str(n))
check = 0
for rnd in range(150):
    for num in nums:
        s = to_hexspeak(num)
        check = (check * 131 + len(s) + rnd) % 1000000007
        for b in s.encode():
            check = (check * 131 + b) % 1000000007
print(f"150 rounds of 100000 numbers: checksum {check}")
