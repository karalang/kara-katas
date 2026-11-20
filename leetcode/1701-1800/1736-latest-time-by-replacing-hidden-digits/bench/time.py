# LeetCode #1736: Latest Time by Replacing Hidden Digits -- the bench
# (time.kara): each hidden digit the largest its neighbours allow.


def maximum_time(time):
    t = list(time)
    if t[0] == "?":
        t[0] = "2" if t[1] == "?" or t[1] <= "3" else "1"
    if t[1] == "?":
        t[1] = "3" if t[0] == "2" else "9"
    if t[3] == "?":
        t[3] = "5"
    if t[4] == "?":
        t[4] = "9"
    return "".join(t)


seed = 1736


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count = 1000000
rounds = 10
times = []
for _ in range(count):
    t = next_random() % 1440
    shown = f"{t // 60 // 10}{t // 60 % 10}:{t % 60 // 10}{t % 60 % 10}"
    hidden = ""
    for c in shown:
        if c != ":" and next_random() % 2 == 0:
            hidden += "?"
        else:
            hidden += c
    times.append(hidden)
total = 0
check = 0
for r in range(rounds):
    for time in times:
        b = maximum_time(time).encode()
        total += b[1] - 48
        check = (check * 31 + b[0] * 1000 + b[1] * 100 + b[3] * 10 + b[4] + r) % 1000000007
print(f"{count} times, {rounds} rounds: hour digits sum to {total}, checksum {check}")
