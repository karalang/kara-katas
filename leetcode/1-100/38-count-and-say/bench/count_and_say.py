"""LeetCode #38 bench — Python (mirror of count_and_say.kara).

Streaming run-length "say" over a growing digit string. Workload: TOTAL times seed the
sequence with the decimal digits of k+1, apply STEPS say-steps, fold a position-weighted
digit signature of the final term into a checksum. Same sink as the Kāra / C / Rust / Go
mirrors — the slow interpreted lane in the runtime table.
"""

TOTAL = 12000
STEPS = 14
MODULUS = 1000000007


def say(s: str) -> str:
    # Run lengths stay <= 9 in this workload (verified max 5), so the count is a
    # single decimal digit appended in place — fair, allocation-free across mirrors.
    out = []
    run_digit = ""
    run_len = 0
    for ch in s:
        if run_len != 0 and ch == run_digit:
            run_len += 1
        else:
            if run_len != 0:
                out.append(chr(ord("0") + run_len))
                out.append(run_digit)
            run_digit = ch
            run_len = 1
    if run_len != 0:
        out.append(chr(ord("0") + run_len))
        out.append(run_digit)
    return "".join(out)


def main() -> None:
    acc = 0
    for k in range(TOTAL):
        cur = str(k + 1)
        for _ in range(STEPS):
            cur = say(cur)
        sig = 0
        for i, ch in enumerate(cur):
            sig += (ord(ch) - ord("0")) * (i + 1)
        acc = (acc * 31 + sig) % MODULUS
    print(acc)


if __name__ == "__main__":
    main()
