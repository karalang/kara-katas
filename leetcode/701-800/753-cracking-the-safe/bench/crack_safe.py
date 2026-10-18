# LeetCode 753 — Cracking the Safe, bench: the ★ arm (an Euler circuit by
# Hierholzer's method), mirrored from crack_safe.kara.


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


def main():
    rounds = 2000
    safes = digits = check = 0
    for _ in range(rounds):
        for n in range(1, 5):
            for k in range(1, 11):
                total = k ** n
                if total <= 4096:
                    safes += 1
                    text = crack_safe(n, k)
                    digits += len(text)
                    for b in text.encode():
                        check = (check * 31 + b) % 1000000007
    print(f"{safes} safes: {digits} digits in all, checksum {check}")


main()
