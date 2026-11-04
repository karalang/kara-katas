# LeetCode #1044: Longest Duplicate Substring -- Python mirror of
# longest_dup.kara (binary search on the length, rolling hash), same
# harness.

BASE = 131
MODULUS = 1_000_000_007


def longest_dup_substring(s):
    data = s.encode()
    low, high = 1, len(data) - 1
    best_start, best_len = 0, 0
    while low <= high:
        length = (low + high) // 2
        start = repeated_window(data, length)
        if start is not None:
            best_start, best_len = start, length
            low = length + 1
        else:
            high = length - 1
    return s[best_start:best_start + best_len]


def repeated_window(data, length):
    n = len(data)
    lead = 1
    for _ in range(1, length):
        lead = lead * BASE % MODULUS
    h = 0
    for i in range(length):
        h = (h * BASE + data[i]) % MODULUS
    seen = {}
    found = None
    start = 0
    while True:
        starts = seen.get(h)
        earlier = starts is not None and any(same(data, j, start, length) for j in starts)
        if earlier:
            if found is None or smaller(data, start, found, length):
                found = start
        else:
            seen.setdefault(h, []).append(start)
        if start + length == n:
            break
        h = (h - data[start] * lead % MODULUS + MODULUS) % MODULUS
        h = (h * BASE + data[start + length]) % MODULUS
        start += 1
    return found


def same(data, a, b, length):
    return data[a:a + length] == data[b:b + length]


def smaller(data, a, b, length):
    return data[a:a + length] < data[b:b + length]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def fold_into(check, answer):
    check = (check * 131 + len(answer) + 1) % 1000000007
    for b in answer.encode():
        check = (check * 131 + b) % 1000000007
    return check


def show(answer):
    if len(answer) <= 24:
        return f'"{answer}"'
    return f'"{answer[0:12]}...{answer[len(answer) - 12:]}" ({len(answer)} letters)'


def random_string(n, k, seed):
    return "".join(chr(ord("a") + next_random(seed) % k) for _ in range(n))


def main():
    examples = [
        "banana",
        "abcd",
        "aa",
        "ab",
        "aaaaa",
        "abcabc",
        "mississippi",
        "abababab",
        "zxyzxyxyz",
        "theeuntheeuntheeun",
    ]
    for s in examples:
        print(f'"{s}" -> {show(longest_dup_substring(s))}')
    for k, most in [(2, 12), (3, 7)]:
        cases = total = check = 0
        for n in range(2, most + 1):
            for code in range(k ** n):
                c = code
                letters = []
                for _ in range(n):
                    letters.append(chr(ord("a") + c % k))
                    c //= k
                answer = longest_dup_substring("".join(letters))
                cases += 1
                total += len(answer)
                check = fold_into(check, answer)
        print(f"every string of 2 to {most} letters from {k}: {cases} cases, total length {total}, checksum {check}")
    seed = [1044]
    total = check = 0
    for _ in range(300):
        n = next_random(seed) % 199 + 2
        k = next_random(seed) % 25 + 2
        answer = longest_dup_substring(random_string(n, k, seed))
        total += len(answer)
        check = fold_into(check, answer)
    print(f"300 random strings: total length {total}, checksum {check}")
    wide = random_string(5000, 26, seed)
    print(f"5000 random letters -> {show(longest_dup_substring(wide))}")
    a, b = "a", "ab"
    while len(b) < 5000:
        a, b = b, b + a
    fib = b[0:5000]
    print(f"5000 letters of the Fibonacci word -> {show(longest_dup_substring(fib))}")


main()
