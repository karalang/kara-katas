# LeetCode #1750: Minimum Length of String After Deleting Similar Ends --
# mirrors ends.kara (the ★ arm): two pointers.


def minimum_length(s):
    b = s.encode()
    left = 0
    right = len(b) - 1
    while left < right and b[left] == b[right]:
        c = b[left]
        while left <= right and b[left] == c:
            left += 1
        while right >= left and b[right] == c:
            right -= 1
    return right - left + 1


seed = 1750


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(size, letters):
    alphabet = "abc"
    if next_random() % 2 == 1:
        n = next_random() % size + 1
        return "".join(alphabet[next_random() % letters] for _ in range(n))
    s = ""
    for _ in range(next_random() % 3):
        s += alphabet[next_random() % letters]
    while len(s) < size:
        letter = alphabet[next_random() % letters]
        before = next_random() % 3 + 1
        after = next_random() % 3 + 1
        s = letter * before + s + letter * after
    return s


def batch(count, size, letters):
    total = 0
    check = 0
    for _ in range(count):
        s = draw(size, letters)
        answer = minimum_length(s)
        total += answer
        check = (check * 31 + answer + len(s)) % 1000000007
    print(f"{count} strings of up to {size} letters from {letters}: lengths add to {total}, checksum {check}")


for s in ["ca", "cabaabac", "aabccabba", "a", "aa", "abcba", "b" * 100000]:
    print(minimum_length(s))
batch(3000, 10, 2)
batch(1000, 100, 3)
batch(20, 100000, 3)
