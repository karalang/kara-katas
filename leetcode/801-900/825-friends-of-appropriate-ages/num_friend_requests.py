# LeetCode 825 — Friends Of Appropriate Ages, by counts by age.
#
# Mirrors num_friend_requests.kara: count the people by age once, test
# every pair of ages with the three conditions, and add a request from
# every person of the first age to every person of the second, but for a
# person and themself.

def asks(x, y):
    return not (2 * y <= x + 14 or y > x or (y > 100 and x < 100))

def num_friend_requests(ages):
    count = [0] * 121
    for a in ages:
        count[a] += 1
    requests = 0
    for x in range(1, 121):
        if count[x] == 0:
            continue
        for y in range(1, 121):
            if count[y] > 0 and asks(x, y):
                requests += count[x] * count[y]
                if x == y:
                    requests -= count[x]
    return requests

seed = 0
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def show(ages):
    print(f"[{', '.join(map(str, ages))}] -> {num_friend_requests(ages)}")

show([16, 16])
show([16, 17, 18])
show([20, 30, 100, 110, 120])
show([1])
show([14, 14, 14])
show([15, 15])
show([99, 101, 100])
show([120, 60, 67, 68, 37, 38])
seed = 825
rand = [1 + next_random() % 120 for _ in range(20000)]
print(f"20000 random ages -> {num_friend_requests(rand)}")
print(f"20000 aged 120 -> {num_friend_requests([120] * 20000)}")
total = 0
check = 0
for _ in range(300):
    n = 1 + next_random() % 30
    ages = [1 + next_random() % 120 for _ in range(n)]
    r = num_friend_requests(ages)
    total += r
    check = (check * 131 + r) % 1000000007
print(f"300 random lists: total {total}, checksum {check}")
