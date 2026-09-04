"""Benchmark lane for LeetCode 316 — Python mirror of bench/remove_duplicate_letters.kara.

Generate N drifting letters once, then PASSES monotone-stack passes (record
each letter's last occurrence, then skip placed letters and pop larger tops
that still have a later copy), each after overwriting one position chosen
from the checksum.
"""

N = 4000000
PASSES = 100
MASK = 1073741823


def lcg(s):
    return (s * 1103515245 + 12345) & 0x7FFFFFFF


def remove_duplicate_letters(bs):
    last = [-1] * 26
    for i, b in enumerate(bs):
        last[b - 97] = i
    on_stack = [False] * 26
    stack = []
    for i, c in enumerate(bs):
        ci = c - 97
        if on_stack[ci]:
            continue
        while stack:
            top = stack[-1]
            if top > c and last[top - 97] > i:
                stack.pop()
                on_stack[top - 97] = False
            else:
                break
        stack.append(c)
        on_stack[ci] = True
    return stack


def main():
    seed = 316
    text = bytearray(N)
    cur = 25
    for i in range(N):
        seed = lcg(seed)
        r = seed // 65536
        if r % 4 != 0:
            cur -= 1
            if cur < 0:
                cur = 25
        else:
            cur = r % 26
        text[i] = cur + 97

    checksum = 0
    for _ in range(PASSES):
        i = checksum % N
        letter = (checksum * 7 + 13) % 26
        saved = text[i]
        text[i] = letter + 97
        out = remove_duplicate_letters(text)
        fold = 0
        for b in out:
            fold = (fold * 131 + b) & MASK
        checksum = (checksum * 31 + fold + len(out)) & MASK
        text[i] = saved
    print(f"checksum {checksum}")


if __name__ == "__main__":
    main()
