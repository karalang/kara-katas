# LeetCode #1307: Verbal Arithmetic Puzzle -- the Python mirror of the ★ arm
# (the sum done a column at a time from the right with its carry, the
# result's letter fixed by each column's sum), with the same harness.
import sys

sys.setrecursionlimit(10000)


def solve(p, col, row, total):
    words, result, leads, digit, taken = p
    if col == len(result):
        return total == 0
    if row == len(words):
        letter = result[col]
        d = total % 10
        if digit[letter] >= 0:
            return digit[letter] == d and solve(p, col + 1, 0, total // 10)
        if taken[d] or (d == 0 and leads[letter]):
            return False
        digit[letter] = d
        taken[d] = True
        ok = solve(p, col + 1, 0, total // 10)
        digit[letter] = -1
        taken[d] = False
        return ok
    if col >= len(words[row]):
        return solve(p, col, row + 1, total)
    letter = words[row][col]
    if digit[letter] >= 0:
        return solve(p, col, row + 1, total + digit[letter])
    for d in range(10):
        if taken[d] or (d == 0 and leads[letter]):
            continue
        digit[letter] = d
        taken[d] = True
        ok = solve(p, col, row + 1, total + d)
        digit[letter] = -1
        taken[d] = False
        if ok:
            return True
    return False


def is_solvable(words, result):
    if any(len(w) > len(result) for w in words):
        return False
    number = {}
    leads = []
    rows = []
    for text in words + [result]:
        row = []
        for c in text:
            if c not in number:
                number[c] = len(number)
                leads.append(False)
            row.append(number[c])
        if len(row) > 1:
            leads[row[0]] = True
        row.reverse()
        rows.append(row)
    result_row = rows.pop()
    p = (rows, result_row, leads, [-1] * len(number), [False] * 10)
    return solve(p, 0, 0, 0)


seed = 1307


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(b):
    return "true" if b else "false"


def main():
    e = [
        is_solvable(["SEND", "MORE"], "MONEY"),
        is_solvable(["SIX", "SEVEN", "SEVEN"], "TWENTY"),
        is_solvable(["LEET", "CODE"], "POINT"),
        is_solvable(["A", "B"], "A"),
        is_solvable(["AB", "CD"], "E"),
        is_solvable(["A", "A"], "B"),
        is_solvable(["AB", "BA"], "CC"),
    ]
    print(" ".join(show(b) for b in e))
    letters = "ABCDEFGHIJ"
    solvable = 0
    check = 0
    for p in range(600):
        count = 2 + next_random() % 3
        words = []
        result = ""
        if p % 2 == 0:
            while True:
                texts = []
                total = 0
                for _ in range(count):
                    length = 1 + next_random() % 3
                    low = 0 if length == 1 else 10 if length == 2 else 100
                    value = low + next_random() % (10 * (1 if low == 0 else low) - low)
                    texts.append(str(value))
                    total += value
                texts.append(str(total))
                digits = []
                for text in texts:
                    for c in text:
                        if c not in digits:
                            digits.append(c)
                if len(digits) <= 6:
                    break
            written = ["".join(letters[digits.index(c)] for c in text) for text in texts]
            result = written.pop()
            words = written
        else:
            k = 2 + next_random() % 4
            for _ in range(count):
                length = 1 + next_random() % 3
                words.append("".join(letters[next_random() % k] for _ in range(length)))
            length = 1 + next_random() % 4
            result = "".join(letters[next_random() % k] for _ in range(length))
        got = is_solvable(words, result)
        if got:
            solvable += 1
        check = (check * 3 + (1 if got else 0)) % 1000000007
    print(f"600 random puzzles: {solvable} solvable, checksum {check}")


main()
