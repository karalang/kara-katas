# Benchmark workload — Python mirror of simplify.kara.
#
# Same N=8 inputs, K=1_000_000 iters cycled by k % N. Sink is the
# sum of the simplified-output string lengths (i64), matching the
# kara/rust/c/go mirrors so all five impls print the same number.


def simplify(s: str) -> str:
    n = len(s)
    starts: list[int] = []
    ends: list[int] = []

    i = 0
    while i < n:
        while i < n and s[i] == '/':
            i += 1
        if i >= n:
            break
        j = i
        while j < n and s[j] != '/':
            j += 1
        length = j - i

        is_dot    = length == 1 and s[i] == '.'
        is_dotdot = length == 2 and s[i] == '.' and s[i + 1] == '.'

        if is_dot:
            pass
        elif is_dotdot:
            if starts:
                starts.pop()
                ends.pop()
        else:
            starts.append(i)
            ends.append(j)
        i = j

    if not starts:
        return "/"
    parts = [s[a:b] for a, b in zip(starts, ends)]
    return "/" + "/".join(parts)


def main() -> None:
    inputs = [
        "/home/",
        "/home/user/Documents/../Pictures",
        "/.../a/../b/c/../d/./",
        "/a/b/c/../..",
        "/a//b////c/d//././/..",
        "/abc_123",
        "/a/b/../c/../../d",
        "/...hidden",
    ]
    n = len(inputs)
    k_iters = 1_000_000

    total = 0
    for k in range(k_iters):
        total += len(simplify(inputs[k % n]))
    print(total)


if __name__ == "__main__":
    main()
