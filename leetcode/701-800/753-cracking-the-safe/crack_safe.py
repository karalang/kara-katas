# LeetCode 753 — Cracking the Safe, mirror of the ★ arm (an Euler circuit
# by Hierholzer's method) and its harness.


def crack_safe(n, k):
    nodes = 1
    for _ in range(n - 1):
        nodes *= k
    used = [0] * nodes
    stack = [(0, -1)]
    digits = []
    while stack:
        node, digit = stack[-1]
        if used[node] < k:
            d = used[node]
            used[node] += 1
            stack.append(((node * k + d) % nodes, d))
        else:
            stack.pop()
            if digit >= 0:
                digits.append(digit)
    out = ["0"] * (n - 1)
    for d in reversed(digits):
        out.append(chr(48 + d))
    return "".join(out)


def judged(text, n, k):
    total = k ** n
    seen = [0] * total
    bad = 0
    for i in range(len(text) - n + 1):
        code = 0
        for j in range(i, i + n):
            d = ord(text[j]) - 48
            if d < 0 or d >= k:
                bad += 1
            code = code * k + d
        if 0 <= code < total:
            seen[code] += 1
    once = sum(1 for c in seen if c == 1)
    size = "shortest" if len(text) == total + n - 1 else "NOT SHORTEST"
    codes = "every code once" if once == total and bad == 0 else "CODES WRONG"
    return f"{len(text)} digits, {size}, {codes}"


def show(n, k):
    print(f"n = {n}, k = {k}: {judged(crack_safe(n, k), n, k)}")


def main():
    for n, k in [(1, 2), (2, 2), (1, 1), (4, 1), (1, 10), (3, 2), (2, 10), (3, 10), (4, 8)]:
        show(n, k)
    safes = digits = good = 0
    for n in range(1, 5):
        for k in range(1, 11):
            if k ** n <= 4096:
                safes += 1
                text = crack_safe(n, k)
                digits += len(text)
                if judged(text, n, k).endswith("shortest, every code once"):
                    good += 1
    print(f"all {safes} safes: {digits} digits in all, {good} shortest with every code once")


main()
