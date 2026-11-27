# LeetCode #1472: Design Browser History -- Python mirror of
# browser_history.kara


class BrowserHistory:
    def __init__(self, homepage):
        self.pages = [homepage]
        self.at = 0
        self.end = 1

    def visit(self, url):
        self.at += 1
        if self.at < len(self.pages):
            self.pages[self.at] = url
        else:
            self.pages.append(url)
        self.end = self.at + 1

    def back(self, steps):
        self.at = max(self.at - steps, 0)
        return self.pages[self.at]

    def forward(self, steps):
        self.at = min(self.at + steps, self.end - 1)
        return self.pages[self.at]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, url):
    for b in url.encode():
        check = (check * 131 + b) % 1000000007
    return check


def main():
    global seed
    b = BrowserHistory("leetcode.com")
    b.visit("google.com")
    b.visit("facebook.com")
    b.visit("youtube.com")
    r1 = b.back(1)
    r2 = b.back(1)
    r3 = b.forward(1)
    b.visit("linkedin.com")
    r4 = b.forward(2)
    r5 = b.back(2)
    r6 = b.back(7)
    print(f"{r1} {r2} {r3} {r4} {r5} {r6}")
    e = BrowserHistory("home.org")
    e1 = e.back(3)
    e2 = e.forward(3)
    e.visit("a.org")
    e.visit("b.org")
    e3 = e.back(2)
    e.visit("c.org")
    e4 = e.forward(1)
    e5 = e.back(1)
    e6 = e.forward(5)
    print(f"{e1} {e2} {e3} {e4} {e5} {e6}")
    seed = 1472
    check = 0
    calls = 0
    for s in range(2000):
        h = BrowserHistory(f"s{s}.home")
        n = 1 + next_random() % 100
        for c in range(n):
            r = next_random() % 3
            steps = 1 + next_random() % 10
            if r == 0:
                h.visit(f"s{s}.p{c}")
            elif r == 1:
                check = fold(check, h.back(steps))
            else:
                check = fold(check, h.forward(steps))
            calls += 1
    print(f"2000 random sessions: {calls} calls, checksum {check}")


main()
