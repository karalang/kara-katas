# LeetCode #1750: Minimum Length of String After Deleting Similar Ends --
# the bench (ends.kara in Python): two pointers.


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


# a random middle of up to 1000 letters from `a` and `b`, wrapped in
# layers of one letter on both sides until the string is `n` long
def draw(n):
    alphabet = "ab"
    middle = "".join(alphabet[next_random() % 2] for _ in range(next_random() % 1000))
    front = []
    back = []
    size = len(middle)
    while size < n:
        letter = alphabet[next_random() % 2]
        before = next_random() % 3 + 1
        after = next_random() % 3 + 1
        front.append(letter * before)
        back.append(letter * after)
        size += before + after
    return "".join(reversed(front)) + middle + "".join(back)


count, rounds, n = 50, 40, 100000
strings = [draw(n) for _ in range(count)]
total = 0
check = 0
for r in range(rounds):
    for s in strings:
        answer = minimum_length(s)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} strings of about {n} letters, {rounds} rounds: lengths add to {total}, checksum {check}")
