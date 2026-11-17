# LeetCode #2232: Minimize Result by Adding Parentheses to Expression --
# the benchmark's Python mirror of parentheses.kara: every place for the
# two parentheses, the first smallest a * (b + c) * d kept.


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


def draw_expression():
    left = next_random() % 8 + 1
    right = next_random() % (9 - left) + 1
    out = []
    for k in range(left + right + 1):
        out.append("+" if k == left else chr(49 + next_random() % 9))
    return "".join(out)


def main():
    expressions = [draw_expression() for _ in range(20000)]
    check = 0
    for _ in range(20):
        # punch: one expression drawn again before each pass over all
        at = next_random() % 20000
        expressions[at] = draw_expression()
        for expression in expressions:
            answer = minimize_result(expression)
            check = (check * 31 + len(answer) + answer.index("(") * 11 + answer.index(")")) % 1000000007
    print(f"20 passes over 20000 expressions: checksum {check}")


main()
