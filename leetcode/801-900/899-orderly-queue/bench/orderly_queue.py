# LeetCode #899 bench: the counts arm (rotations compared in place,
# letters counted) on 1,000 strings of 1,000 letters, LeetCode's largest,
# each a random piece of 1 to 4 letters written over and over with one
# letter changed at a random place, so that rotations agree for long
# stretches before they differ. Every string is asked with k = 1, and
# with k = 2 as well. The same algorithm as orderly_queue.kara.


def orderly_queue(s, k):
    b = s.encode()
    n = len(b)
    if k == 1:
        best = 0
        for i in range(1, n):
            d = 0
            while d < n and b[(i + d) % n] == b[(best + d) % n]:
                d += 1
            if d < n and b[(i + d) % n] < b[(best + d) % n]:
                best = i
        return "".join(chr(b[(best + j) % n]) for j in range(n))
    count = [0] * 26
    for c in b:
        count[c - 97] += 1
    return "".join(chr(97 + letter) * count[letter] for letter in range(26))


seed = 899


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def checksum(s, check):
    for ch in s:
        check = (check * 131 + ord(ch)) % 1000000007
    return check


def main():
    check = 0
    for _ in range(1000):
        p = 1 + next_random() % 4
        piece = [chr(97 + next_random() % 26) for _ in range(p)]
        changed = next_random() % 1000
        letter = chr(97 + next_random() % 26)
        s = "".join(letter if i == changed else piece[i % p] for i in range(1000))
        check = checksum(orderly_queue(s, 1), check)
        check = checksum(orderly_queue(s, 2), check)
    print(f"1000 strings of 1000 letters, k = 1 and 2: checksum {check}")


main()
