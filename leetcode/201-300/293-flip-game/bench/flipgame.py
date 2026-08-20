"""Benchmark twin for LeetCode #293 — same algorithm as flipgame.kara."""

LEN, BOARDS = 64, 40000


def next_rand(s):
    return (s * 1103515245 + 12345) & 2147483647


def main():
    seed = 20260820
    total_states = checksum = 0
    for d in (15, 50, 85):
        for _ in range(BOARDS):
            cs = []
            for _ in range(LEN):
                seed = next_rand(seed)
                cs.append("+" if ((seed // 65536) % 100) < d else "-")
            s = "".join(cs)
            out = [s[:i] + "--" + s[i + 2:]
                   for i in range(LEN - 1) if s[i] == "+" and s[i + 1] == "+"]
            total_states += len(out)
            for t in out:
                checksum = (checksum * 31 + len(t)) % 1000000007
    print(f"states {total_states} checksum {checksum}")


if __name__ == "__main__":
    main()
