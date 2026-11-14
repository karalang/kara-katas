# LeetCode #1531: String Compression II -- mirrors compression.kara (the ★
# arm): best[i][j], the shortest encoding of the suffix from i with j
# deletions left, by deleting place i or keeping a run that starts there.
# O(n^2 k).


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, letters):
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        over = next_random() % letters + 1
        s = "".join(chr(97 + next_random() % over) for _ in range(n))
        k = next_random() % (n + 1)
        check = mix(check, get_length_of_optimal_compression(s, k))
    print(f"{count} strings of 1 to {most} letters over up to {letters}: checksum {check}")


def main():
    global seed
    examples = [
        ("aaabcccd", 2),
        ("aabbaa", 2),
        ("aaaaaaaaaaa", 0),
        ("abcdefghijklmnopqrstuvwxyz", 25),
        ("a", 1),
        ("aaaaaaaaaab", 1),
    ]
    for s, k in examples:
        print(f"{s}, k = {k} -> {get_length_of_optimal_compression(s, k)}")
    print(f"100 a's, k = 0 -> {get_length_of_optimal_compression('a' * 100, 0)}")
    seed = 1531
    batch(3000, 12, 3)
    batch(300, 100, 4)


main()
