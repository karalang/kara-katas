# LeetCode #125 bench harness — Python reference (interpreted, single-thread).
#
# Same allocating filter-then-compare as the Kara mirror. Sink = ITERS.

ITERS = 3_000_000


def is_palindrome(s):
    clean = [c for c in s if c.isalnum()]
    clean = [c.lower() for c in clean]
    return clean == clean[::-1]


def main():
    input_s = "A man, a plan, a canal: Panama" * 8
    total = 0
    for _ in range(ITERS):
        total += 1 if is_palindrome(input_s) else 0
    print(total)


if __name__ == "__main__":
    main()
