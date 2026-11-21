# LeetCode #2424: Longest Uploaded Prefix -- the Python mirror of the ★
# arm: a flag for each video and the prefix so far, moved on by `longest`
# past every flag set beyond it.

seed = 2424


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class LUPrefix:
    def __init__(self, n):
        self.uploaded = [False] * (n + 2)
        self.prefix = 0

    def upload(self, video):
        self.uploaded[video] = True

    def longest(self):
        while self.uploaded[self.prefix + 1]:
            self.prefix += 1
        return self.prefix


def run(n, calls):
    server = LUPrefix(n)
    answers = []
    for kind, video in calls:
        if kind == 0:
            server.upload(video)
        else:
            answers.append(server.longest())
    return answers


def random_script(n, ask):
    order = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = (next_random() * 32768 + next_random()) % (i + 1)
        order[i], order[j] = order[j], order[i]
    calls = []
    for v in order:
        calls.append((0, v))
        if next_random() % ask == 0:
            calls.append((1, 0))
    return calls


def show(answers):
    return "[" + ",".join(str(a) for a in answers) + "]"


def digest(answers):
    h = 0
    for a in answers:
        h = (h * 31 + a) % 1000000007
    return f"{len(answers)} answers: {h} {sum(answers)}"


def main():
    print(show(run(4, [(0, 3), (1, 0), (0, 1), (1, 0), (0, 2), (1, 0)])))
    print(show(run(3, [(0, 1), (1, 0), (0, 2), (1, 0), (0, 3), (1, 0)])))
    print(show(run(3, [(0, 3), (1, 0), (0, 2), (1, 0), (0, 1), (1, 0)])))
    print(show(run(4, [(1, 0), (0, 2), (0, 3), (0, 4), (1, 0), (0, 1), (1, 0)])))
    print(digest(run(100000, random_script(100000, 1))))
    print(digest(run(100000, random_script(100000, 10))))
    blocks = []
    for b in range(1000):
        for k in range(100):
            blocks.append((0, 100 * b + 100 - k))
        blocks.append((1, 0))
    print(digest(run(100000, blocks)))
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 12
        ask = 1 + next_random() % 3
        for a in run(n, random_script(n, ask)):
            check = (check * 31 + a + 1) % 1000000007
            total += a
        check = (check * 31 + 100) % 1000000007
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
