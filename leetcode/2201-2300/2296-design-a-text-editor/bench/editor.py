# LeetCode #2296: Design a Text Editor -- the bench, the ★ arm in Python.
# Two stacks of letters: `left` holds the text before the cursor in
# order, `right` the text after it reversed.


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


def main():
    editors = [calls_of(20000) for _ in range(10)]
    check = 0
    for _ in range(10):
        for calls in editors:
            for answer in run(calls):
                for b in answer.encode():
                    check = (check * 131 + b) % 1000000007
                check = (check * 131 + 1) % 1000000007
    print(f"10 passes over 10 editors of 2 * 10^4 calls: checksum {check}")


main()
