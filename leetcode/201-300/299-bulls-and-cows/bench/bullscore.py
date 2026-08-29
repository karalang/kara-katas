"""Benchmark mirror of bullscore.kara - LeetCode #299, Bulls and Cows.

Same algorithm: build boards once, then 12 scoring passes over a flat digit
array. Deliberately not idiomatic Python (no Counter, no comprehensions in the
hot loop) so the comparison is algorithm-for-algorithm. See ../README.md.
"""

N_PAIRS = 400000
PASSES = 12
WIDTH = 4
ALPHABET = 4


def lcg(state: int) -> int:
    return (state * 1103515245 + 12345) & 0x7FFFFFFF


def main() -> None:
    total = N_PAIRS * WIDTH
    secrets = [0] * total
    guesses = [0] * total

    state = 20299
    for i in range(total):
        state = lcg(state)
        secrets[i] = (state // 65536) % ALPHABET
        state = lcg(state)
        guesses[i] = (state // 65536) % ALPHABET

    checksum = 0
    for _pass in range(PASSES):
        for p in range(N_PAIRS):
            base = p * WIDTH
            s_left = [0] * ALPHABET
            g_left = [0] * ALPHABET
            bulls = 0
            cows = 0

            for k in range(WIDTH):
                sd = secrets[base + k]
                gd = guesses[base + k]
                if sd == gd:
                    bulls += 1
                else:
                    s_left[sd] += 1
                    g_left[gd] += 1

            for d in range(ALPHABET):
                cows += s_left[d] if s_left[d] < g_left[d] else g_left[d]

            checksum = (checksum * 31 + bulls * 7 + cows) % 1000000007

    print(f"pairs {N_PAIRS} passes {PASSES} checksum {checksum}")


if __name__ == "__main__":
    main()
