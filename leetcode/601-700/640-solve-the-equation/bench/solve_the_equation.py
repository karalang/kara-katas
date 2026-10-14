# Benchmark for #640: mirror of solve_the_equation.kara (the ★ arm: each
# side read once into a count of x and a constant) on the same workload.

ROUNDS = 200000


def side(text):
    xs = 0
    constant = 0
    i = 0
    n = len(text)
    while i < n:
        sign = 1
        if text[i] == "+" or text[i] == "-":
            if text[i] == "-":
                sign = -1
            i += 1
        value = 0
        digits = 0
        while i < n and "0" <= text[i] <= "9":
            value = value * 10 + ord(text[i]) - 48
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


def random_side(terms):
    parts = []
    xs = 0
    constant = 0
    for t in range(terms):
        minus = next_random() % 2 == 0
        if minus:
            parts.append("-")
        elif t > 0:
            parts.append("+")
        sign = -1 if minus else 1
        value = next_random() % 100
        if next_random() % 2 == 0:
            parts.append(f"{value}x")
            xs += sign * value
        else:
            parts.append(f"{value}")
            constant += sign * value
    return "".join(parts), xs, constant


def main():
    equations = []
    for _ in range(20):
        left, a, b = random_side(125)
        right, c, d = random_side(125)
        text = f"{left}={right}"
        if a != c:
            # Kāra's `%` truncates toward zero, as C's does.
            rem = abs(d - b) % abs(a - c)
            if d - b < 0:
                rem = -rem
            if rem > 0:
                text = f"{text}-{rem}"
            elif rem < 0:
                text = f"{text}+{-rem}"
        equations.append(text)
    solved = 0
    total = 0
    for r in range(ROUNDS):
        answer = solve_equation(equations[r % 20])
        if answer.startswith("x="):
            solved += 1
            total += int(answer[2:])
    print(f"20 equations, {ROUNDS} rounds: {solved} solved, x adding to {total}")


main()
