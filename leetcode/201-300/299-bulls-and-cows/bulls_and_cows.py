"""LeetCode 299 - Bulls and Cows.

Mirror of bulls_and_cows.kara: same two-pass tally, same reconciliation, same
output, line for line. Kept algorithm-for-algorithm rather than idiomatic so the
benchmark comparison is honest - a Python solution would normally reach for
collections.Counter and the & operator, which is the same computation but hands
the whole loop to C and measures something different.
"""


def digit_index(c: str) -> int:
    return ord(c) - ord("0")


def bulls_and_cows(secret: str, guess: str) -> str:
    n = len(secret)
    bulls = 0
    cows = 0

    s_left = [0] * 10
    g_left = [0] * 10

    for i in range(n):
        if secret[i] == guess[i]:
            # Spent as a bull, so it enters neither tally.
            bulls += 1
        else:
            s_left[digit_index(secret[i])] += 1
            g_left[digit_index(guess[i])] += 1

    for d in range(10):
        cows += s_left[d] if s_left[d] < g_left[d] else g_left[d]

    return f"{bulls}A{cows}B"


def report(secret: str, guess: str) -> None:
    print(f"secret {secret}  guess {guess}  ->  {bulls_and_cows(secret, guess)}")


def main() -> None:
    report("1807", "7810")
    report("1123", "0111")
    report("1", "0")
    report("1", "1")
    report("11", "10")
    report("11", "01")
    report("1122", "2211")
    report("1122", "1222")
    report("0000", "0000")
    report("0000", "1111")
    report("", "")
    report("1234567890", "0987654321")


if __name__ == "__main__":
    main()
