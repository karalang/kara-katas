# LeetCode #2232: Minimize Result by Adding Parentheses to Expression --
# the mirror of parentheses.kara: every place for the two parentheses,
# the first smallest a * (b + c) * d kept.


def minimize_result(expression):
    plus = expression.index("+")
    left = expression[:plus]
    right = expression[plus + 1:]
    best = None
    answer = ""
    for i in range(len(left)):
        for j in range(1, len(right) + 1):
            a = 1 if i == 0 else int(left[:i])
            b = int(left[i:])
            c = int(right[:j])
            d = 1 if j == len(right) else int(right[j:])
            value = a * (b + c) * d
            if best is None or value < best:
                best = value
                answer = f"{left[:i]}({left[i:]}+{right[:j]}){right[j:]}"
    return answer


seed = 2232


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw_digits(count):
    return "".join(chr(49 + next_random() % 9) for _ in range(count))


def main():
    for expression in ["247+38", "12+34", "999+999", "1+1", "11+11", "12345678+9", "1+23456789"]:
        print(f"{expression} -> {minimize_result(expression)}")
    check = 0
    for _ in range(3000):
        left = next_random() % 8 + 1
        right = next_random() % (9 - left) + 1
        expression = f"{draw_digits(left)}+{draw_digits(right)}"
        for b in minimize_result(expression).encode():
            check = (check * 31 + b) % 1000000007
    print(f"3000 expressions: checksum {check}")
    wrapped = 0
    split = 0
    for a in range(11, 100):
        for b in range(11, 100):
            if a % 10 != 0 and b % 10 != 0:
                answer = minimize_result(f"{a}+{b}")
                if answer.startswith("(") and answer.endswith(")"):
                    wrapped += 1
                else:
                    split += 1
    print(f"6561 two-digit sums: {wrapped} wrapped whole, {split} split")


main()
