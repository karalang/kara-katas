# LeetCode #2259: Remove Digit From Number to Maximize Result -- Python
# mirror of the ★ arm (remove.kara): the first occurrence followed by a
# larger digit, else the last occurrence. Output is byte-identical to the
# Kara arms.


def remove_digit(number, digit):
    last = 0
    for i in range(len(number)):
        if number[i] == digit:
            last = i
            if i + 1 < len(number) and number[i + 1] > digit:
                break
    return number[:last] + number[last + 1:]


# ---- test harness ---------------------------------------------------------

seed = 2259


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(length, top):
    number = "".join(chr(ord("1") + next_random() % top) for _ in range(length))
    return number, number[next_random() % length]


def fold(check, s):
    h = check
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return (h * 131 + 7) % 1000000007


def main():
    examples = [("123", "3"), ("1231", "1"), ("551", "5"), ("99", "9"), ("19", "1"), ("2998", "9"), ("3334333", "3")]
    for number, digit in examples:
        print(f"{number} without one {digit} -> {remove_digit(number, digit)}")
    check = 0
    kept_last = 0
    for t in range(5000):
        tops = [2, 3, 4, 9]
        length = next_random() % 19 + 2
        number, digit = draw(length, tops[t % 4])
        answer = remove_digit(number, digit)
        last = number.rindex(digit)
        if answer == number[:last] + number[last + 1:]:
            kept_last += 1
        check = fold(check, answer)
    print(f"5000 numbers: {kept_last} lose their last occurrence, checksum {check}")
    long = [remove_digit("7" * 100, "7")]
    long.append(remove_digit("".join(chr(ord("9") - i // 12) for i in range(100)), "5"))
    number, digit = draw(100, 9)
    long.append(remove_digit(number, digit))
    for s in long:
        print(f"{len(s)} digits: {s[:30]}... checksum {fold(0, s)}")


main()
