# LeetCode #2048 -- the ★ arm as a benchmark; mirror of beautiful.kara.


def is_balanced(x):
    counts = [0] * 10
    y = x
    while y > 0:
        counts[y % 10] += 1
        y //= 10
    for d in range(10):
        if counts[d] != 0 and counts[d] != d:
            return False
    return True


def next_beautiful_number(n):
    x = n + 1
    while not is_balanced(x):
        x += 1
    return x


def main():
    calls = total = check = 0
    for k in range(1000):
        x = next_beautiful_number(k * 1000 + k * 7 % 1000)
        calls += 1
        total += x
        check = (check * 31 + x) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
