# LeetCode #640: Solve the Equation -- Python mirror of the ★ arm.
#
# Each side read once into a count of x and a constant.


def side(text):
    xs = 0
    constant = 0
    i = 0
    n = len(text)
    while i < n:
        sign = 1
        if text[i] in "+-":
            if text[i] == "-":
                sign = -1
            i += 1
        value = 0
        digits = 0
        while i < n and text[i].isdigit():
            value = value * 10 + int(text[i])
            digits += 1
            i += 1
        if i < n and text[i] == "x":
            xs += sign * (1 if digits == 0 else value)
            i += 1
        else:
            constant += sign * value
    return xs, constant


def solve_equation(equation):
    eq = equation.index("=")
    a, b = side(equation[:eq])
    c, d = side(equation[eq + 1:])
    if a == c:
        return "Infinite solutions" if b == d else "No solution"
    return f"x={(d - b) // (a - c)}"


seed = 640


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_side(terms, most):
    text = ""
    xs = 0
    constant = 0
    for t in range(terms):
        minus = next_random() % 2 == 0
        if minus:
            text += "-"
        elif t > 0:
            text += "+"
        sign = -1 if minus else 1
        value = next_random() % (most + 1)
        if next_random() % 2 == 0:
            if value == 1 and next_random() % 4 != 0:
                text += "x"
            else:
                text += f"{value}x"
            xs += sign * value
        else:
            text += f"{value}"
            constant += sign * value
    return text, xs, constant


def rem_of(p, q):
    # Kāra's `%` truncates toward zero, as C's does.
    r = abs(p) % abs(q)
    return -r if p < 0 else r


def evened(text, rem):
    if rem > 0:
        return f"{text}-{rem}"
    if rem < 0:
        return f"{text}+{-rem}"
    return text


def ask(equation):
    print(f"{equation} -> {solve_equation(equation)}")


def main():
    for e in ["x+5-3+x=6+x-2", "x=x", "2x=x", "x=x+2", "3=x", "0x=5", "-x=-1",
              "1+2=3", "1+2=4", "2x+3=x-4", "100x-250=50x+250", "0x=0x",
              "-x+3x-2x=0"]:
        ask(e)
    solved = total = none = every = 0
    for _ in range(300):
        left, a, b = random_side(1 + next_random() % 6, 12)
        right, c, d = random_side(1 + next_random() % 6, 12)
        text = f"{left}={right}"
        if a != c:
            text = evened(text, rem_of(d - b, a - c))
        answer = solve_equation(text)
        if answer == "No solution":
            none += 1
        elif answer == "Infinite solutions":
            every += 1
        else:
            solved += 1
            total += int(answer[2:])
    print(f"300 random equations: {solved} solved (x adding to {total}), "
          f"{none} with no solution, {every} with every x")
    left, a, b = random_side(190, 9)
    right, c, d = random_side(190, 9)
    text = f"{left}={right}"
    if a != c:
        text = evened(text, rem_of(d - b, a - c))
    print(f"{len(text)} characters -> {solve_equation(text)}")


main()
