# LeetCode #2067: Number of Equal Count Substrings -- Python mirror of the
# ★ arm's benchmark (count.kara): 60 texts of 30000 letters from 1 to 26
# kinds, half in runs of `count`, count 1 to 7.


def equal_count_substrings(s, count):
    b = s.encode()
    n = len(b)
    total = 0
    for k in range(1, 27):
        length = k * count
        if length > n:
            break
        seen = [0] * 26
        exact = 0
        for i in range(n):
            c = b[i] - 97
            seen[c] += 1
            if seen[c] == count:
                exact += 1
            elif seen[c] == count + 1:
                exact -= 1
            if i >= length:
                d = b[i - length] - 97
                if seen[d] == count:
                    exact -= 1
                seen[d] -= 1
                if seen[d] == count:
                    exact += 1
            if i + 1 >= length and exact == k:
                total += 1
    return total


# ---- bench -----------------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def text_of(n, k, count, p, seed):
    letters = "abcdefghijklmnopqrstuvwxyz"
    out = []
    length = 0
    while length < n:
        c = letters[next_random(seed) % k]
        run = count if next_random(seed) % 100 < p else 1
        out.append(c * min(run, n - length))
        length += min(run, n - length)
    return "".join(out)


def main():
    seed = [2067]
    total = 0
    check = 0
    for t in range(60):
        count = t % 7 + 1
        a = equal_count_substrings(text_of(30000, t % 26 + 1, count, 50, seed), count)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"60 texts: sum {total}, checksum {check}")


main()
