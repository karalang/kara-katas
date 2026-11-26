# LeetCode #1797: Design Authentication Manager -- the ★ arm in Python: a
# dict from each token to the second it expires.


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


def run(calls, life, step, check):
    ttl = 1 + next_random() % life
    m = AuthenticationManager(ttl)
    made = 0
    now = 0
    for _ in range(calls):
        now += 1 + next_random() % step
        pick = next_random() % 10
        if pick < 4:
            m.generate(name(made), now)
            made += 1
        elif pick < 8:
            m.renew(name(next_random() % (made + 2)), now)
        else:
            check = (check * 31 + m.count_unexpired_tokens(now)) % 1000000007
    return check


def main():
    m = AuthenticationManager(5)
    m.renew("aaa", 1)
    m.generate("aaa", 2)
    first = m.count_unexpired_tokens(6)
    m.generate("bbb", 7)
    m.renew("aaa", 8)
    m.renew("bbb", 10)
    print(f"{first} {m.count_unexpired_tokens(15)}")
    m = AuthenticationManager(5)
    m.generate("a", 1)
    before = m.count_unexpired_tokens(5)
    m.renew("a", 6)
    after = m.count_unexpired_tokens(7)
    m.generate("b", 8)
    m.renew("b", 12)
    m.renew("zz", 13)
    print(f"{before} {after} {m.count_unexpired_tokens(16)} {m.count_unexpired_tokens(17)}")
    m = AuthenticationManager(100000000)
    for k in range(1000):
        m.generate(name(k), k + 1)
    total = 0
    for k in range(1000):
        total += m.count_unexpired_tokens(100000000 - 999 + k)
    wide = run(2000, 100000000, 50000, 0)
    print(f"the most: {total} {wide}")
    check = 0
    for _ in range(3000):
        calls = 1 + next_random() % 40
        check = run(calls, 30, 10, check)
    print(f"3000 random runs: checksum {check}")


main()
