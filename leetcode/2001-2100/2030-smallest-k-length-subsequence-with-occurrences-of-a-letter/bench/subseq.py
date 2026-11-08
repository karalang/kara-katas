# LeetCode #2030: Smallest K-Length Subsequence With Occurrences of a Letter
# -- the ★ arm in Python, the same algorithm and workload as subseq.kara.


def smallest_subsequence(s, k, letter, repetition):
    data = s.encode()
    want = ord(letter)
    n = len(data)
    remain = data.count(want)
    stack = []
    have = 0
    for i in range(n):
        c = data[i]
        while (stack and stack[-1] > c and len(stack) - 1 + n - i >= k
               and (stack[-1] != want or have - 1 + remain >= repetition)):
            if stack.pop() == want:
                have -= 1
        if len(stack) < k:
            if c == want:
                stack.append(c)
                have += 1
            elif k - len(stack) > repetition - have:
                stack.append(c)
        if c == want:
            remain -= 1
    return bytes(stack).decode()


seed = 2030


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    texts = []
    for a in range(10):
        span = 2 + 3 * a
        out = []
        c = 0
        for _ in range(50000):
            r = next_random() % 10
            if r < 4:
                c = (c + 1) % span
            elif r < 7:
                c = next_random() % span
            out.append(chr(97 + c))
        texts.append("".join(out))
    calls = kept = check = 0
    for rnd in range(20):
        for a in range(10):
            s = texts[a]
            k = (rnd * 2477 + a * 911) % 50000 + 1
            letter = chr(97 + (rnd + a) % (2 + 3 * a))
            copies = s.count(letter)
            repetition = (rnd * 131 + a * 17) % min(k, copies) + 1
            got = smallest_subsequence(s, k, letter, repetition).encode()
            calls += 1
            n = len(got)
            kept += n
            check = (check * 31 + n) % 1000000007
            check = (check * 31 + got[0] + got[n // 2] + got[n - 1]) % 1000000007
    print(f"{calls} calls: {kept} letters kept, checksum {check}")


main()
