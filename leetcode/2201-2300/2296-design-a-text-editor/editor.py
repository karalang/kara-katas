# LeetCode #2296: Design a Text Editor -- the ★ arm in Python. Two stacks
# of letters: `left` holds the text before the cursor in order, `right`
# the text after it reversed.


class TextEditor:
    def __init__(self):
        self.left = []
        self.right = []

    def add_text(self, text):
        self.left.extend(text)

    def delete_text(self, k):
        n = min(k, len(self.left))
        for _ in range(n):
            self.left.pop()
        return n

    def cursor_left(self, k):
        for _ in range(min(k, len(self.left))):
            self.right.append(self.left.pop())
        return self.tail()

    def cursor_right(self, k):
        for _ in range(min(k, len(self.right))):
            self.left.append(self.right.pop())
        return self.tail()

    def tail(self):
        return "".join(self.left[len(self.left) - min(len(self.left), 10):])


def run(calls):
    editor = TextEditor()
    answers = []
    for kind, k, text in calls:
        if kind == 0:
            editor.add_text(text)
        elif kind == 1:
            answers.append(str(editor.delete_text(k)))
        elif kind == 2:
            answers.append(editor.cursor_left(k))
        else:
            answers.append(editor.cursor_right(k))
    return answers


seed = 2296


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def calls_of(count):
    calls = []
    for _ in range(count):
        kind = next_random() % 4
        k = next_random() % 40 + 1
        text = ""
        if kind == 0:
            text = "".join(chr(ord("a") + next_random() % 26) for _ in range(k))
        calls.append((kind, k, text))
    return calls


def tally(answers, check):
    c = check
    for answer in answers:
        for b in answer.encode():
            c = (c * 131 + b) % 1000000007
        c = (c * 131 + 1) % 1000000007
    return c


def main():
    examples = [
        [(0, 0, "leetcode"), (1, 4, ""), (0, 0, "practice"), (3, 3, ""), (2, 8, ""), (1, 10, ""), (2, 2, ""), (3, 6, "")],
        [(1, 5, ""), (2, 3, ""), (3, 3, ""), (0, 0, "ab"), (1, 40, ""), (2, 1, ""), (3, 1, "")],
        [(0, 0, "hello"), (2, 2, ""), (0, 0, "XYZ"), (3, 40, ""), (2, 4, ""), (1, 2, ""), (3, 1, "")],
        [(0, 0, "abcdefghijklmnopqrstuvwxyz"), (2, 3, ""), (3, 2, ""), (2, 40, ""), (3, 13, ""), (1, 13, ""), (3, 40, "")],
    ]
    for calls in examples:
        print("|".join(run(calls)))
    answered = 0
    check = 0
    for _ in range(3000):
        count = next_random() % 30 + 1
        answers = run(calls_of(count))
        answered += len(answers)
        check = tally(answers, check)
    print(f"3000 small editors: {answered} answers, checksum {check}")
    answered = 0
    check = 0
    for _ in range(5):
        answers = run(calls_of(20000))
        answered += len(answers)
        check = tally(answers, check)
    print(f"5 editors of 2 * 10^4 calls: {answered} answers, checksum {check}")


main()
