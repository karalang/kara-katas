# LeetCode #71: Simplify Path — Python mirror of simplify.kara.
#
# One-pass scan over the input chars. Maintain a stack of (start, end)
# index pairs into the input that name the components currently on the
# canonical path. Components are maximal non-'/' runs; '.' is skipped,
# '..' pops one entry (or stays at root), every other run is pushed.
# At end-of-scan, walk the stack to reconstruct the output:
# "/" + components joined by "/", or "/" alone if the stack is empty.


def simplify(s: str) -> str:
    n = len(s)
    starts: list[int] = []
    ends: list[int] = []

    i = 0
    while i < n:
        # Skip the slash run between components.
        while i < n and s[i] == '/':
            i += 1
        if i >= n:
            break
        # Consume the non-slash run [i, j).
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


def report(s: str) -> None:
    print(f'simplify "{s}" -> "{simplify(s)}"')


def main() -> None:
    # Canonical LeetCode spec examples.
    report("/home/")
    report("/home//foo/")
    report("/home/user/Documents/../Pictures")
    report("/../")
    report("/.../a/../b/c/../d/./")

    # Root edge cases.
    report("/")
    report("//")
    report("///")

    # Many-slashes-and-dots compressions.
    report("/a/./b/../../c/")
    report("/a//b////c/d//././/..")

    # Pop past root saturates at "/".
    report("/../../../")
    report("/a/../../b")

    # Single-component, single-slash retention rules.
    report("/a")
    report("/a/")
    report("/abc_123")

    # Multi-dot runs that are NOT '.' or '..' — they're file names.
    report("/...")
    report("/....")
    report("/.hidden")
    report("/..hidden")
    report("/...hidden")

    # Single dot at end + middle, trailing-slash collapse.
    report("/./")
    report("/a/./b/./c/.")

    # Dotdot interleaved with files.
    report("/a/b/c/../..")
    report("/a/b/../c/../../d")


if __name__ == "__main__":
    main()
