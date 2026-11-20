# LeetCode #2384: Largest Palindromic Number -- the Python mirror of
# palindrome.kara.


def largest_palindromic(num):
    count = [0] * 10
    for c in num:
        count[ord(c) - 48] += 1
    half = []
    for d in range(9, -1, -1):
        if d == 0 and not half:
            break
        for _ in range(count[d] // 2):
            half.append(chr(48 + d))
    out = list(half)
    for d in range(9, -1, -1):
        if count[d] % 2 == 1:
            out.append(chr(48 + d))
            break
    if not out:
        return "0"
    out.extend(reversed(half))
    return "".join(out)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, s):
    for b in s:
        check = (check * 31 + ord(b)) % 1000000007
    return check


def digits(n, zeros, top):
    out = []
    for _ in range(n):
        if next_random() % 10 < zeros:
            out.append("0")
        else:
            out.append(chr(48 + next_random() % top))
    return "".join(out)


def main():
    global seed
    print(largest_palindromic("444947137"))
    print(largest_palindromic("00009"))
    print(f"{largest_palindromic('0')} {largest_palindromic('00')} {largest_palindromic('000')}")
    print(f"{largest_palindromic('1234567890')} {largest_palindromic('010010')}")
    seed = 2384
    big = largest_palindromic(digits(100000, 0, 10))
    zeros = ["0"] * 100000
    zeros[50000] = "5"
    lone = largest_palindromic("".join(zeros))
    print(f"{len(big)} digits, checksum {fold(0, big)}; {lone}")
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 10
        zeros = next_random() % 10
        answer = largest_palindromic(digits(n, zeros, top))
        check = fold(check, answer)
        total += len(answer)
    print(f"3000 strings: checksum {check}, {total} digits in all")


if __name__ == "__main__":
    main()
