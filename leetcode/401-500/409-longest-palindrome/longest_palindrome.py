# LeetCode #409: Longest Palindrome -- mirror of longest_palindrome.kara
# (letter counts).


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


def show(s):
    print(f'"{s}": {longest_palindrome(s)}')


show("abccccdd")
show("a")
show("Aa")
show("bb")
show("ccc")
show("abc")
show("AAAAAA")
show("aaabbbccc")
show("racecar")
show("aAbBcCdD")
show("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
show("civilwartestingwhetherthatnationoranynationsoconceivedandsodedicated")
alphabet = b"abcABC"
total = 0
checksum = 0
for _ in range(3000):
    n = 1 + step() % 60
    s = "".join(chr(alphabet[step() % 6]) for _ in range(n))
    answer = longest_palindrome(s)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"3000 random strings: total {total}, checksum {checksum}")
