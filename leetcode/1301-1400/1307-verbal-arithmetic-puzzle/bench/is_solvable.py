# LeetCode #1307 bench in Python: the ★ arm (the sum done a column at a time
# from the right with its carry) on the same 40 passes of 50 puzzles.
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


def main():
    check = 0
    for pass_no in range(40):
        seed = check

        def next_random():
            nonlocal seed
            seed = (seed * 1103515245 + 12345) % 2147483648
            return seed // 65536

        solvable = 0
        for p in range(50):
            letter = list("ABCDEFGHIJ")
            for k in range(9, 0, -1):
                j = next_random() % (k + 1)
                letter[k], letter[j] = letter[j], letter[k]
            count = 2 + next_random() % 4
            numbers = []
            for _ in range(count):
                digits = 1 + next_random() % 6
                low = 10 ** (digits - 1)
                value = next_random() % 10 if digits == 1 else low + next_random() % (9 * low)
                numbers.append(value)
            numbers.append(sum(numbers))
            texts = ["".join(letter[ord(c) - ord("0")] for c in str(v)) for v in numbers]
            result = texts.pop()
            if p % 2 == 1:
                chars = list(result)
                at = next_random() % len(chars)
                chars[at] = letter[next_random() % 10]
                result = "".join(chars)
            if is_solvable(texts, result):
                solvable += 1
        check = (check * 31 + solvable + pass_no) % 1000000007
    print(f"40 passes of 50 puzzles: checksum {check}")


main()
