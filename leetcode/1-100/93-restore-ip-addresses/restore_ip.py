"""LeetCode #93: Restore IP Addresses — backtracking over the four segments.

Mirror of restore_ip.kara. Place one segment at a time from `start`, trying lengths
1/2/3, validating (1-3 digits, no leading zero unless "0", value <= 255), and recursing
for the next part. Four parts consuming the whole string is a complete address; dots are
woven in as `path` is built. Same nine cases and output shape (a `"input": count`
header, each address on its own line, then a `sink:` fold) so the files diff
line-for-line.
"""

from __future__ import annotations


def backtrack(s: list[int], n: int, start: int, part: int, path: str, out: list[str]) -> None:
    if part == 4:
        if start == n:
            out.append(path)
        return
    length = 1
    while length <= 3:
        if start + length > n:
            break
        val = 0
        seg = ""
        for i in range(length):
            d = s[start + i] - 48
            val = val * 10 + d
            seg += str(d)
        valid = (length == 1 or s[start] != 48) and val <= 255
        if valid:
            newpath = seg if part == 0 else f"{path}.{seg}"
            backtrack(s, n, start + length, part + 1, newpath, out)
        length += 1


def restore(string: str) -> list[str]:
    s = list(string.encode())
    out: list[str] = []
    backtrack(s, len(s), 0, 0, "", out)
    return out


def report(string: str, acc: list[int]) -> None:
    ips = restore(string)
    count = len(ips)
    print(f'"{string}": {count}')
    for ip in ips:
        print(ip)
    a = (acc[0] * 131 + (count + 1)) % 1000000007
    for ip in ips:
        for b in ip.encode():
            a = (a * 131 + b) % 1000000007
        a = (a * 131 + 7) % 1000000007
    acc[0] = a


def main() -> None:
    acc = [0]
    report("25525511135", acc)
    report("0000", acc)
    report("101023", acc)
    report("1111", acc)
    report("255255255255", acc)
    report("010010", acc)
    report("1", acc)
    report("1234567890123", acc)
    report("", acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
