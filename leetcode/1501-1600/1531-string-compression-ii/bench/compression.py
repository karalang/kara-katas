# LeetCode #1531: String Compression II -- bench: the ★ arm over 300 random
# strings of 1 to 100 letters, each over its own 1 to 4 letters with k from
# 0 to its length, built once and answered 10 times.


def run_length(count):
    if count == 1:
        return 1
    if count < 10:
        return 2
    if count < 100:
        return 3
    return 4


def get_length_of_optimal_compression(s, k):
    b = s.encode()
    n = len(b)
    best = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(k + 1):
            shortest = n + 1
            if j > 0:
                shortest = best[i + 1][j - 1]
            same = 0
            other = 0
            for end in range(i, n):
                if b[end] == b[i]:
                    same += 1
                else:
                    other += 1
                if other > j:
                    break
                shortest = min(shortest, run_length(same) + best[end + 1][j - other])
            best[i][j] = shortest
    return best[0][k]


seed = 1531


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    cases = []
    for _ in range(300):
        n = next_random() % 100 + 1
        over = next_random() % 4 + 1
        s = "".join(chr(97 + next_random() % over) for _ in range(n))
        cases.append((s, next_random() % (n + 1)))
    check = 0
    for _ in range(10):
        for s, k in cases:
            check = mix(check, get_length_of_optimal_compression(s, k))
    print(f"10 passes over 300 strings of up to 100 letters: checksum {check}")


main()
