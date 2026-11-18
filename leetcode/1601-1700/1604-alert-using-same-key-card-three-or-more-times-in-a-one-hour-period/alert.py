# LeetCode #1604: Alert Using Same Key-Card Three or More Times in a One
# Hour Period -- the Python mirror of alert.kara (the ★ arm): each name's
# minutes gathered and sorted, the names in order. Its output is
# byte-identical to the Kāra arms'.


def minutes(t):
    h, m = t.split(":", 1)
    return int(h) * 60 + int(m)


def alert_names(key_name, key_time):
    uses = {}
    for name, time in zip(key_name, key_time):
        uses.setdefault(name, []).append(minutes(time))
    out = []
    for name in sorted(uses):
        times = sorted(uses[name])
        if any(times[i] - times[i - 2] <= 60 for i in range(2, len(times))):
            out.append(name)
    return out


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def big(self):
        a = self.next()
        return a * 32768 + self.next()


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


NAMES = ["daniel", "luis", "alice", "bob", "john", "leslie", "clare", "anna"]


def batch(count, people, uses, span, rng):
    check = alerts = swipes = 0
    for _ in range(count):
        n = rng.big() % uses + 1
        start = rng.next() % (1440 - span + 1)
        names, times = [], []
        for _ in range(n):
            who = rng.next() % people
            names.append(NAMES[who] if who < 8 else f"{NAMES[who % 8]}{who // 8}")
            t = start + rng.next() % span
            times.append(f"{t // 60:02}:{t % 60:02}")
        for name in alert_names(names, times):
            alerts += 1
            for b in name.encode():
                check = mix(check, b)
            check = mix(check, 0)
        check = mix(check, 1)
        swipes += n
    print(f"{count} days of up to {uses} swipes by up to {people} names: {swipes} swipes, {alerts} alerts, checksum {check}")


def main():
    examples = [
        (["daniel", "daniel", "daniel", "luis", "luis", "luis", "luis"], ["10:00", "10:40", "11:00", "09:00", "11:00", "13:00", "15:00"]),
        (["alice", "alice", "alice", "bob", "bob", "bob", "bob"], ["12:01", "12:00", "18:00", "21:00", "21:20", "21:30", "23:00"]),
        (["john", "john", "john"], ["23:58", "23:59", "00:01"]),
        (["leslie", "leslie", "leslie", "clare", "clare", "clare", "clare"], ["13:00", "13:20", "14:00", "18:00", "18:51", "19:30", "19:49"]),
        (["anna", "anna", "anna", "anna"], ["08:00", "08:30", "09:01", "09:31"]),
    ]
    for names, times in examples:
        print(f"[{', '.join(alert_names(names, times))}]")
    rng = Rng(1604)
    batch(3000, 4, 8, 120, rng)
    batch(300, 50, 2000, 1440, rng)
    batch(3, 2000, 100000, 1440, rng)


main()
