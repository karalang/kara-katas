# LeetCode #1817: Finding the Users Active Minutes -- the ★ arm in Python:
# each user's distinct minutes gathered in a set under the user's id, and
# the answer's entry for j counts the users with j distinct minutes.


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


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's two examples
    print(show(finding_users_active_minutes([[0, 5], [1, 2], [0, 2], [0, 5], [1, 3]], 5)), show(finding_users_active_minutes([[1, 1], [2, 2], [2, 3]], 4)))
    # the edges: one log; one user many times in one minute; ids and
    # minutes at their largest; a k past every user's minutes
    print(
        show(finding_users_active_minutes([[7, 7]], 1)),
        show(finding_users_active_minutes([[3, 9], [3, 9], [3, 9]], 2)),
        show(finding_users_active_minutes([[1000000000, 100000], [0, 1], [1000000000, 1]], 3)),
        show(finding_users_active_minutes([[1, 1], [1, 2], [2, 1]], 6)),
    )
    # the constraints' most: 10^4 logs, one user over 10^4 minutes, and
    # 10^4 users with a minute each
    one = [[5, m] for m in range(10000)]
    many = [[u, 1] for u in range(10000)]
    a = finding_users_active_minutes(one, 10000)
    b = finding_users_active_minutes(many, 3)
    print("the most:", a[9999], sum(a), show(b))
    # 3000 random cases of 1 to 40 logs over 1 to 6 users and 1 to 9 minutes
    seed = [1817]
    check = 0
    for _ in range(3000):
        n = 1 + next_random(seed) % 40
        users = 1 + next_random(seed) % 6
        span = 1 + next_random(seed) % 9
        logs = [[next_random(seed) % users, next_random(seed) % span] for _ in range(n)]
        k = span + next_random(seed) % 3
        for x in finding_users_active_minutes(logs, k):
            check = (check * 31 + x) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
