# LeetCode #929: Unique Email Addresses -- one walk per address and a set
# (Python mirror).


def num_unique_emails(emails):
    seen = set()
    for e in emails:
        out = []
        domain = False
        tagged = False
        for c in e:
            if domain:
                out.append(c)
            elif c == "@":
                domain = True
                out.append(c)
            elif c == "+":
                tagged = True
            elif c != "." and not tagged:
                out.append(c)
        seen.add("".join(out))
    return len(seen)


seed = 929


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, emails):
    print(f"{name}: {num_unique_emails(emails)}")


def random_email():
    s = ""
    letters = 1 + next_random() % 3
    for _ in range(letters):
        if next_random() % 3 == 0:
            s += "."
        s += "a" if next_random() % 2 == 0 else "b"
    if next_random() % 2 == 0:
        s += "+"
        for _ in range(next_random() % 4):
            s += "ab.+"[next_random() % 4]
    d = next_random() % 6
    return s + ["@b.com", "@ab.com", "@xy.com", "@x.y.com", "@x+y.com", "@x+b.com"][d]


def main():
    show("example 1", ["test.email+alex@leetcode.com", "test.e.mail+bob.cathy@leetcode.com", "testemail+david@lee.tcode.com"])
    show("example 2", ["a@leetcode.com", "b@leetcode.com", "c@leetcode.com"])
    show("one address", ["a@b.com"])
    show("one address four ways", ["ab@x.com", "a.b@x.com", "ab+c@x.com", "a.b+c.d@x.com"])
    show("dots in the domain", ["a@b.c.com", "a@bc.com"])
    show("a '+' in the domain", ["a@b+c.com", "a@b.com"])
    show("a tag of dots and '+'s", ["a+.+.@x.com", "a@x.com", "a+@x.com"])
    show("dots around one letter", ["..a..+b@x.com", "a@x.com", "b@x.com"])
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 100
        emails = [random_email() for _ in range(n)]
        a = num_unique_emails(emails)
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"300 random lists: answers summing to {total}, checksum {check}")
    distinct = []
    same = []
    for t in range(100):
        local = ""
        v = t
        for _ in range(7):
            local += "a." if v % 2 == 0 else "b."
            v //= 2
        while len(local) < 93:
            local += "."
        distinct.append(local + "@ab.com")
        other = "a" + "." * (t % 40) + "b+"
        while len(other) < 94:
            other += "c"
        same.append(other + "@x.com")
    print(f"100 addresses of {len(distinct[0])} characters, all different: {num_unique_emails(distinct)}")
    print(f"100 addresses of {len(same[0])} characters, one address: {num_unique_emails(same)}")


main()
