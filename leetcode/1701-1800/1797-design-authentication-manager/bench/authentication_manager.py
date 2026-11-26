# LeetCode #1797: Design Authentication Manager -- the bench in Python: the
# ★ arm, a dict from each token to the second it expires, over 50 random
# scripts of 2000 calls built once, 2000 runs.


class AuthenticationManager:
    def __init__(self, time_to_live):
        self.ttl = time_to_live
        self.expiry = {}

    def generate(self, token_id, current_time):
        self.expiry[token_id] = current_time + self.ttl

    def renew(self, token_id, current_time):
        e = self.expiry.get(token_id)
        if e is not None and e > current_time:
            self.expiry[token_id] = current_time + self.ttl

    def count_unexpired_tokens(self, current_time):
        return sum(1 for e in self.expiry.values() if e > current_time)


seed = 1797


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def name(k):
    s = ""
    while True:
        s += "abcdefghijklmnopqrstuvwxyz"[k % 26]
        k //= 26
        if k == 0:
            return s


def main():
    scripts = []
    for _ in range(50):
        ttl = 1 + next_random() % 100000
        calls = []
        made = 0
        now = 0
        for _ in range(2000):
            now += 1 + next_random() % 100
            pick = next_random() % 10
            if pick < 4:
                calls.append((0, name(made), now))
                made += 1
            elif pick < 8:
                calls.append((1, name(next_random() % (made + 2)), now))
            else:
                calls.append((2, "", now))
        scripts.append((ttl, calls))
    check = 0
    for run in range(2000):
        ttl, calls = scripts[(check + run) % 50]
        m = AuthenticationManager(ttl)
        for op, token, t in calls:
            if op == 0:
                m.generate(token, t)
            elif op == 1:
                m.renew(token, t)
            else:
                check = (check * 31 + m.count_unexpired_tokens(t)) % 1000000007
    print(f"2000 runs over 50 scripts of 2000 calls: checksum {check}")


main()
