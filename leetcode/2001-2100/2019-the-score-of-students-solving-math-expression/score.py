# LeetCode #2019: The Score of Students Solving Math Expression -- Python
# mirror of the ★ arm (score.kara). The right answer read left to right; every
# value a wrong order can give found by an interval DP, values above 1000
# dropped.


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


# ---- test harness ----------------------------------------------------------

seed = 2019


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_expression(count, top, times):
    s = []
    for i in range(count):
        if i > 0:
            s.append('*' if next_random() % 10 < times else '+')
        s.append(chr(ord('0') + next_random() % (top + 1)))
    return ''.join(s)


def random_answers(count, top):
    return [next_random() % (top + 1) for _ in range(count)]


def show(v):
    return '[' + ', '.join(str(x) for x in v) + ']'


def main():
    examples = [
        ("7+3*1*2", [20, 13, 42]),
        ("3+5*2", [13, 0, 10, 13, 13, 16, 16]),
        ("6+0*1", [12, 9, 6, 4, 8, 6]),
        ("1+2*3+4", [11, 13, 15, 21, 15, 0]),
        ("9", [9, 0, 1000]),
        ("9*9*9*9+1*0", [0, 1, 6561, 729, 6562]),
        ("2*3+4*5", [26, 50, 70, 46, 9]),
    ]
    for s, answers in examples:
        print(f"\"{s}\", {show(answers)} -> {score_of_students(s, answers)}")
    total = 0
    check = 0
    for _ in range(1500):
        count = next_random() % 6 + 1
        top = next_random() % 9 + 1
        times = next_random() % 11
        s = random_expression(count, top, times)
        n_answers = next_random() % 8 + 1
        answers = random_answers(n_answers, next_random() % 25 + 1)
        points = score_of_students(s, answers)
        total += points
        check = (check * 31 + points) % 1000000007
    print(f"1500 expressions of up to 6 digits: {total} points, checksum {check}")
    total = 0
    check = 0
    for a in range(6):
        count = [11, 11, 10, 11, 9, 11][a]
        top = [9, 3, 5, 2, 9, 1][a]
        times = [5, 3, 7, 6, 4, 10][a]
        s = random_expression(count, top, times)
        answers = random_answers(10000, [1000, 300, 1000, 200, 1000, 20][a])
        points = score_of_students(s, answers)
        total += points
        check = (check * 31 + points) % 1000000007
    print(f"6 expressions of up to 11 digits, 10000 answers each: {total} points, checksum {check}")


main()
