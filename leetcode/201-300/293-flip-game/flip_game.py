"""Oracle mirror for LeetCode 293 — same algorithm as flip_game.kara.

Test the pair first, allocate only where a move exists.
"""


def next_states(s):
    out = []
    for i in range(len(s) - 1):
        if s[i] == "+" and s[i + 1] == "+":
            out.append(s[:i] + "--" + s[i + 2:])
    return out


def report(s):
    print(f"{s} -> [{', '.join(next_states(s))}]")


def main():
    for s in ["++++", "+", "-", "", "----", "++", "+++",
              "+-+-+", "++-++", "+++++", "-++-"]:
        report(s)


if __name__ == "__main__":
    main()
