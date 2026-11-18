# LeetCode #1604: Alert Using Same Key-Card Three or More Times in a One
# Hour Period -- the bench in Python, mirroring alert.kara: each name's
# minutes gathered, the names and each list sorted.


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


def main():
    rng = Rng(1604)
    days = []
    for _ in range(30):
        names, times = [], []
        for _ in range(100000):
            who = rng.big() % 20000
            names.append(NAMES[who] if who < 8 else f"{NAMES[who % 8]}{who // 8}")
            t = rng.big() % 1440
            times.append(f"{t // 60:02}:{t % 60:02}")
        days.append((names, times))
    check = alerts = 0
    for names, times in days:
        for name in alert_names(names, times):
            alerts += 1
            for b in name.encode():
                check = mix(check, b)
            check = mix(check, 0)
    print(f"30 days of 100000 swipes by 20000 names: {alerts} alerts, checksum {check}")


main()
