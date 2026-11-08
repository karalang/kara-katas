# LeetCode #2019: The Score of Students Solving Math Expression -- the ★ arm's
# benchmark, a mirror of score.kara.


def score_of_students(s, answers):
    digits = [ord(c) - ord('0') for c in s[0::2]]
    ops = list(s[1::2])
    n = len(digits)
    total = 0
    product = digits[0]
    for i in range(n - 1):
        if ops[i] == '+':
            total += product
            product = digits[i + 1]
        else:
            product *= digits[i + 1]
    correct = total + product
    values = [[set() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        values[i][i].add(digits[i])
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cell = set()
            for k in range(i, j):
                for a in values[i][k]:
                    for b in values[k + 1][j]:
                        v = a + b if ops[k] == '+' else a * b
                        if v <= 1000:
                            cell.add(v)
            values[i][j] = cell
    points = 0
    for answer in answers:
        if answer == correct:
            points += 5
        elif answer in values[0][n - 1]:
            points += 2
    return points


seed = 2019


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    expressions = []
    answer_lists = []
    for e in range(200):
        top = e % 9 + 1
        times = e % 7 + 2
        s = []
        for i in range(16):
            if i > 0:
                s.append('*' if next_random() % 10 < times else '+')
            s.append(chr(ord('0') + next_random() % (top + 1)))
        expressions.append(''.join(s))
        answer_lists.append([next_random() % 1001 for _ in range(2000)])
    calls = total = check = 0
    for _ in range(10):
        for e in range(len(expressions)):
            points = score_of_students(expressions[e], answer_lists[e])
            calls += 1
            total += points
            check = (check * 31 + points) % 1000000007
    print(f"{calls} calls: {total} points, checksum {check}")


main()
