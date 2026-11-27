# LeetCode #1817: Finding the Users Active Minutes -- the bench in Python:
# the ★ arm over 5000 calls on runs of 5000 to 9999 logs cut from one list
# of 10^4 logs over 1000 users and 100 minutes, built once, each run's
# length drawn from the checksum so far.


def finding_users_active_minutes(logs, k):
    minutes = {}
    for user, at in logs:
        minutes.setdefault(user, set()).add(at)
    answer = [0] * k
    for seen in minutes.values():
        answer[len(seen) - 1] += 1
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1817]
    base = []
    for _ in range(10000):
        user = next_random(seed) % 1000
        base.append([user, next_random(seed) % 100])
    check = 0
    for call in range(5000):
        n = 5000 + (check + call) % 5000
        for x in finding_users_active_minutes(base[:n], 100):
            check = (check * 31 + x) % 1000000007
    print(f"5000 calls: checksum {check}")


main()
