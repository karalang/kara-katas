"""Oracle mirror for LeetCode 292 — same algorithm as nim_game.kara.

Losing positions are exactly the multiples of 4: from a multiple every move of
1, 2 or 3 lands on a non-multiple, and from a non-multiple you can always take
n % 4 and hand one back.
"""


def can_win_nim(n):
    return (n % 4) != 0


def report(n):
    print(f"n={n} -> {str(can_win_nim(n)).lower()}")


def main():
    for n in range(1, 13):
        report(n)
    report(2147483647)
    report(2147483644)
    report(0)


if __name__ == "__main__":
    main()
