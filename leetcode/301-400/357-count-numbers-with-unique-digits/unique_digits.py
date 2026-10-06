# LeetCode #357 -- mirror of unique_digits.kara (count by position).


def count_unique(n, base):
    total = 1
    run = base - 1
    nxt = base - 1
    k = 1
    while k <= n and k <= base:
        total += run
        run *= nxt
        nxt -= 1
        k += 1
    return total


def main():
    for n in range(0, 9):
        print(f"n = {n}: {count_unique(n, 10)}")
    for base in range(2, 8):
        row = [str(count_unique(n, base)) for n in range(0, base + 2)]
        print(f"base {base}: {' '.join(row)}")


main()
