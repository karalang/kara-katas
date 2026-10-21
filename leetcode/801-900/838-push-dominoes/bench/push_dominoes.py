# Benchmark for #838: Push Dominoes -- the ★ arm (the stretches between pushes).
#
# Mirrors push_dominoes.kara: the walk goes from push to push, with an L
# imagined before the line and an R after it. Between two pushes the same
# way every domino falls that way; between an R and an L the two halves
# fall inward.


def push_dominoes(dominoes):
    d = list(dominoes)
    n = len(d)
    left = -1
    left_push = 'L'
    for right in range(n + 1):
        right_push = 'R' if right == n else d[right]
        if right_push == '.':
            continue
        if left_push == right_push:
            for i in range(left + 1, right):
                d[i] = right_push
        elif left_push == 'R':
            i = left + 1
            j = right - 1
            while i < j:
                d[i] = 'R'
                d[j] = 'L'
                i += 1
                j -= 1
        left = right
        left_push = right_push
    return ''.join(d)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # 16 lines drawn once, each of LeetCode's longest, 10^5 dominoes,
    # line g pushing each domino left with chance 1 + 4g in 200 and right
    # with the same chance. Each round settles the next line and reads 16
    # dominoes of the result.
    count = 16
    rounds = 1300
    n = 100000
    seed = [838]
    lines = []
    for g in range(count):
        pushed = 1 + 4 * g
        s = []
        for _ in range(n):
            r = next_random(seed) % 200
            s.append('L' if r < pushed else 'R' if r < 2 * pushed else '.')
        lines.append(''.join(s))
    fallen = 0
    checksum = 0
    for round_ in range(rounds):
        out = push_dominoes(lines[round_ % count]).encode()
        for t in range(16):
            b = out[(round_ * 7919 + t * 6151) % n]
            if b != 46:
                fallen += 1
            checksum = (checksum * 31 + b) % 1000000007
    print(f"{rounds} rounds of {count} lines: {fallen} of the dominoes read fallen, checksum {checksum}")


main()
