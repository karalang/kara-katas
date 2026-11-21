# LeetCode #2514: Count Anagrams -- benchmark mirror of the ★ arm
# (anagrams.kara): 20 sentences of 10^5 characters built once, then the
# passes, each asking every sentence from the place the checksum picks.
MOD = 1000000007


def power(base, exponent):
    result, b, e = 1, base % MOD, exponent
    while e > 0:
        if e % 2 == 1:
            result = result * b % MOD
        b = b * b % MOD
        e //= 2
    return result


def count_anagrams(s):
    factorial = [1] * (len(s) + 1)
    for i in range(1, len(s) + 1):
        factorial[i] = factorial[i - 1] * i % MOD
    answer = 1
    for word in s.split(" "):
        counts = [0] * 26
        for b in word.encode():
            counts[b - 97] += 1
        answer = answer * factorial[len(word)] % MOD
        for c in counts:
            answer = answer * power(factorial[c], MOD - 2) % MOD
    return answer


seed = 2514


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sentences = []
    for _ in range(20):
        text = []
        size = 0
        while True:
            length = next_random() % 200 + 1
            if size + 1 + length > 100000:
                break
            if size > 0:
                size += 1
            text.append("".join(chr(97 + next_random() % 26) for _ in range(length)))
            size += length
        sentences.append(" ".join(text))
    passes = 4
    check = 0
    for p in range(passes):
        start = check % 20
        for k in range(20):
            check = (check * 31 + count_anagrams(sentences[(start + k) % 20]) + p) % 1000000007
    print(f"{passes} passes over 20 sentences of 10^5: checksum {check}")


main()
