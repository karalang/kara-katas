"""Benchmark twin for LeetCode #294 — same algorithm as flipgame2.kara.

PARITY NOTE. Memoized backtracking, fresh dict per board, successors built one
character at a time to match Kara's append-only String. Slow enough that the
harness runs it only under KARA_BENCH_INCLUDE_PY=1.
"""

LEN = 22
BOARDS = 300


def next_rand(s):
    return (s * 1103515245 + 12345) & 2147483647


def next_states(s):
    n = len(s)
    out = []
    for i in range(n - 1):
        if s[i] == "+" and s[i + 1] == "+":
            t = []
            for j in range(n):
                t.append("-" if j == i or j == i + 1 else s[j])
            out.append("".join(t))
    return out


def can_win(s, memo):
    v = memo.get(s)
    if v is not None:
        return v
    for t in next_states(s):
        if not can_win(t, memo):
            memo[s] = True
            return True
    memo[s] = False
    return False


def main():
    seed = 20260821
    wins = 0
    checksum = 0
    for d in (15, 50, 85):
        for _ in range(BOARDS):
            chars = []
            for _ in range(LEN):
                seed = next_rand(seed)
                chars.append("+" if ((seed // 65536) % 100) < d else "-")
            s = "".join(chars)
            memo = {}
            if can_win(s, memo):
                wins += 1
            checksum = (checksum * 31 + len(memo)) % 1000000007
    print(f"wins {wins} checksum {checksum}")


if __name__ == "__main__":
    main()
