"""Benchmark mirror of LeetCode #320 — same mask walk as
bench/generalized_abbreviation.kara."""

WORD_LEN = 20
PASSES = 8
MODULUS = 1073741789


def main() -> None:
    sink = 0
    total_chars = 0

    for p in range(PASSES):
        bs = bytes(((i * 7 + p * 11) % 26) + ord("a") for i in range(WORD_LEN))
        buf = bytearray(WORD_LEN + 8)

        limit = 1 << WORD_LEN
        acc = 0
        chars = 0

        for mask in range(limit):
            length = 0
            run = 0
            for i in range(WORD_LEN):
                if mask & (1 << i):
                    run += 1
                else:
                    if run > 0:
                        if run >= 10:
                            buf[length] = (run // 10) + 48
                            length += 1
                        buf[length] = (run % 10) + 48
                        length += 1
                        run = 0
                    buf[length] = bs[i]
                    length += 1
            if run > 0:
                if run >= 10:
                    buf[length] = (run // 10) + 48
                    length += 1
                buf[length] = (run % 10) + 48
                length += 1

            for j in range(length):
                acc = (acc * 131 + buf[j]) % MODULUS
            acc = (acc * 131 + 7) % MODULUS
            chars += length

        sink = (sink * 1000003 + acc) % MODULUS
        total_chars += chars

    print(f"sink {sink} chars {total_chars}")


if __name__ == "__main__":
    main()
