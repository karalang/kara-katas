# LeetCode #2332: The Latest Time to Catch a Bus -- the bench, the ★ arm
# in Python. Both lists sorted into copies, the buses fill in order from
# the earliest passengers; the last bus's departure if it leaves with
# room, else its last passenger's time, then a step back past every
# passenger standing at the time tried. O((n + m) log(n + m)).


def latest_time_catch_the_bus(buses, passengers, capacity):
    buses = sorted(buses)
    passengers = sorted(passengers)
    nxt = 0
    aboard = 0
    for bus in buses:
        aboard = 0
        while aboard < capacity and nxt < len(passengers) and passengers[nxt] <= bus:
            aboard += 1
            nxt += 1
    latest = buses[-1] if aboard < capacity else passengers[nxt - 1]
    k = nxt - 1
    while k >= 0 and passengers[k] == latest:
        latest -= 1
        k -= 1
    return latest


def scrambled(index):
    return index * 2654435761 % 2147483647 + 2


def main():
    cases = []
    for k in range(10):
        base = k * 150000
        buses = [scrambled(base + i) for i in range(50000)]
        passengers = [scrambled(base + i) for i in range(50000, 150000)]
        cases.append((buses, passengers))
    check = 0
    for p in range(5):
        for k in range(10):
            buses, passengers = cases[k]
            check = (check * 31 + latest_time_catch_the_bus(buses, passengers, 1 + (k + p) % 5)) % 1000000007
    print(f"5 passes over 10 cases of 5*10^4 buses and 10^5 passengers: checksum {check}")


main()
