# LeetCode #1472: Design Browser History -- bench, Python mirror of
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


seed = 1472


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, url):
    for b in url.encode():
        check = (check * 131 + b) % 1000000007
    return check


def main():
    pool = [f"site{i}.example.com" for i in range(1000)]
    check = 0
    for _ in range(400):
        h = BrowserHistory("home.example.com")
        for _ in range(5000):
            r = next_random() % 3
            x = next_random()
            if r == 0:
                h.visit(pool[x % 1000])
            elif r == 1:
                check = fold(check, h.back(1 + x % 10))
            else:
                check = fold(check, h.forward(1 + x % 10))
    print(f"400 sessions of 5000 calls: checksum {check}")


main()
