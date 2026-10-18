# LeetCode #721: Accounts Merge -- union-find over the emails.
#
# A mirror of accounts_merge.kara (the ★ arm) and its harness.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def canonical(merged):
    return sorted(" ".join(account) for account in merged)


def show(accounts):
    print(" | ".join(canonical(accounts_merge(accounts))))


def random_accounts(count, most, pool, seed):
    names = ["Ada", "Bo", "Cy", "Di"]
    accounts = []
    for _ in range(count):
        who = next_random(seed) % 4
        account = [names[who]]
        n = 1 + next_random(seed) % most
        for _ in range(n):
            e = 4 * (next_random(seed) % (pool // 4)) + who
            account.append(f"u{e}@m.co")
        accounts.append(account)
    return accounts


def summary(merged):
    sizes = [len(a) - 1 for a in merged]
    return f"{len(merged)} people, {sum(sizes)} emails, the most {max(sizes)}"


def main():
    show([
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ])
    show([
        ["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"],
        ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"],
        ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"],
        ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"],
        ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"],
    ])
    show([["Al", "al@m.co"]])
    show([["Al", "al@m.co", "al@m.co"], ["Al", "al@m.co"]])
    show([["Al", "a@m.co", "b@m.co"], ["Al", "c@m.co", "d@m.co"], ["Al", "b@m.co", "c@m.co"]])
    show([["Al", "x@m.co"], ["Al", "y@m.co"]])
    show([["Bo", "d@m.co", "c@m.co"], ["Al", "b@m.co", "a@m.co"], ["Bo", "e@m.co", "d@m.co"]])
    chain = [["Zed", f"z{i}@m.co", f"z{i + 1}@m.co"] for i in range(999, -1, -1)]
    print(f"a chain of 1000 accounts: {summary(accounts_merge(chain))}")
    seed = [721]
    wide = random_accounts(1000, 3, 8000, seed)
    print(f"1000 accounts of up to 3 emails over 8000: {summary(accounts_merge(wide))}")
    dense = random_accounts(1000, 9, 400, seed)
    print(f"1000 accounts of up to 9 emails over 400: {summary(accounts_merge(dense))}")
    total = 0
    for _ in range(300):
        count = 1 + next_random(seed) % 30
        most = 1 + next_random(seed) % 4
        pool = 4 + 4 * (next_random(seed) % 20)
        lines = canonical(accounts_merge(random_accounts(count, most, pool, seed)))
        for line in lines:
            for c in line:
                total = (total * 31 + ord(c)) % 1000000007
            total = (total * 31 + 10) % 1000000007
        total = (total * 131 + len(lines)) % 1000000007
    print(f"300 random account lists: checksum {total}")


main()
