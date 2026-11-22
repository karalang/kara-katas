# LeetCode #2710: Remove Trailing Zeros From a String -- the Python
# mirror of the star arm (zeros.kara): an index walks back from the end
# over the zeros, and the digits before it are the answer.


def remove_trailing_zeros(num):
    end = len(num)
    while num[end - 1] == "0":
        end -= 1
    return num[:end]


seed = 2710


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_number(n, zeros_in_4):
    digits = [chr(ord("1") + next_random() % 9)]
    for _ in range(n - 1):
        if next_random() % 4 < zeros_in_4:
            digits.append("0")
        else:
            digits.append(chr(ord("0") + next_random() % 10))
    return "".join(digits)


def fold(check, text):
    for c in text:
        check = (check * 131 + ord(c)) % 1000000007
    return (check * 131 + len(text)) % 1000000007


print(remove_trailing_zeros("51230100"))
print(remove_trailing_zeros("123"))
print(remove_trailing_zeros("1"))
print(remove_trailing_zeros("10"))
print(len(remove_trailing_zeros("1" + "0" * 999)))
print(len(remove_trailing_zeros("9" * 1000)))
print(remove_trailing_zeros("1" + "0" * 67 + "1"))
print(remove_trailing_zeros("10203000"))
total = 0
check = 0
for _ in range(3000):
    n = next_random() % 1000 + 1
    num = random_number(n, next_random() % 4)
    if next_random() % 2 == 0:
        num += "0" * (next_random() % 20)
    if len(num) > 1000:
        num = num[:1000]
    out = remove_trailing_zeros(num)
    total += len(num) - len(out)
    check = fold(check, out)
print(f"3000 numbers: {total} zeros removed, checksum {check}")
