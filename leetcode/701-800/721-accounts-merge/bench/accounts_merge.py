# LeetCode #721: Accounts Merge -- union-find over the emails.
# Benchmark mirror of the Kara star arm: every email numbered the first
# time it is seen, each account's emails joined in a union-find, then the
# emails gathered by their root, each group sorted under its name.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root


def accounts_merge(accounts):
    ids, emails, owner, parent = {}, [], [], []
    for account in accounts:
        first = -1
        for email in account[1:]:
            if email not in ids:
                ids[email] = len(emails)
                parent.append(len(emails))
                emails.append(email)
                owner.append(account[0])
            e = ids[email]
            if first < 0:
                first = e
            else:
                a, b = find(parent, first), find(parent, e)
                if a != b:
                    parent[b] = a
    groups = {}
    for e in range(len(emails)):
        groups.setdefault(find(parent, e), []).append(emails[e])
    return [[owner[root]] + sorted(group) for root, group in groups.items()]


def main():
    names = ["Ada", "Bo", "Cy", "Di"]
    seed = [721]
    lists = []
    for _ in range(20):
        accounts = []
        for _ in range(1000):
            who = next_random(seed) % 4
            account = [names[who]]
            n = 1 + next_random(seed) % 4
            for _ in range(n):
                account.append(f"u{4 * (next_random(seed) % 2000) + who}@m.co")
            accounts.append(account)
        lists.append(accounts)
    total = 0
    for rnd in range(50):
        for d in range(20):
            i = (rnd * 7919 + d * 104729) % 1000
            j = (i + 1) % 1000
            while lists[d][j][0] != lists[d][i][0]:
                j = (j + 1) % 1000
            lists[d][i][-1] = lists[d][j][1]
            merged = accounts_merge(lists[d])
            total += len(merged)
            for person in merged:
                total += len(person[1])
    print(f"50 rounds of 20 lists of 1000 accounts: sum {total}")


main()
