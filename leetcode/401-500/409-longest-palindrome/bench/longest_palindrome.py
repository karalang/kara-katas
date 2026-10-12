# Benchmark for #409: mirror of longest_palindrome.kara (letter counts).
import sys


def longest_palindrome(s):
    counts = [0] * 128
    for b in s.encode():
        counts[b] += 1
    length = 0
    odd = False
    for i in range(128):
        length += counts[i] // 2 * 2
        if counts[i] % 2 == 1:
            odd = True
    return length + 1 if odd else length


seed = 409


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    queries = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
    size = 2000000
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = "".join(letters[step() % 52] for _ in range(size))
    total = 0
    checksum = 0
    for _ in range(queries):
        n = 1000 + step() % 1001
        hi = step()
        lo = step()
        start = (hi * 32768 + lo) % (size - n + 1)
        answer = longest_palindrome(text[start:start + n])
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{queries} slices of a {size}-letter text: total {total}, checksum {checksum}")


main()
