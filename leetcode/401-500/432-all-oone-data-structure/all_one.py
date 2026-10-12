# LeetCode #432: All O`one Data Structure -- mirror of all_one.kara (a
# list of count buckets).


class Bucket:
    def __init__(self, count):
        self.count = count
        self.keys = set()
        self.prev = None
        self.next = None


def link_after(at, count):
    b = Bucket(count)
    after = at.next
    b.next = after
    after.prev = b
    at.next = b
    b.prev = at
    return b


def unlink(b):
    b.prev.next = b.next
    b.next.prev = b.prev


def any_key(b):
    for k in b.keys:
        return k
    return ""


class AllOne:
    def __init__(self):
        self.head = Bucket(0)
        self.tail = Bucket(-1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.bucket_of = {}

    def inc(self, key):
        cur = self.bucket_of.get(key, self.head)
        after = cur.next
        up = after if after.count == cur.count + 1 else link_after(cur, cur.count + 1)
        up.keys.add(key)
        self.bucket_of[key] = up
        if cur.count > 0:
            cur.keys.discard(key)
            if not cur.keys:
                unlink(cur)

    def dec(self, key):
        cur = self.bucket_of[key]
        if cur.count == 1:
            del self.bucket_of[key]
        else:
            before = cur.prev
            down = before if before.count == cur.count - 1 else link_after(before, cur.count - 1)
            down.keys.add(key)
            self.bucket_of[key] = down
        cur.keys.discard(key)
        if not cur.keys:
            unlink(cur)

    def get_max_key(self):
        return any_key(self.tail.prev)

    def get_min_key(self):
        return any_key(self.head.next)


def check(kind, got, counts):
    if not counts:
        return f"{kind} none" + ("" if got == "" else " FAILED")
    want = max(counts.values()) if kind == "max" else min(counts.values())
    holders = sum(1 for c in counts.values() if c == want)
    mark = "" if counts.get(got) == want else " FAILED"
    if holders == 1:
        return f"{kind} {got}{mark}"
    return f"{kind} one of {holders} at {want}{mark}"


def apply(ds, op, key, counts, answers):
    if op == "inc":
        ds.inc(key)
        counts[key] = counts.get(key, 0) + 1
    elif op == "dec":
        ds.dec(key)
        if counts[key] == 1:
            del counts[key]
        else:
            counts[key] -= 1
    elif op == "max":
        answers.append(check("max", ds.get_max_key(), counts))
    else:
        answers.append(check("min", ds.get_min_key(), counts))


def run(script):
    ds = AllOne()
    counts = {}
    answers = []
    for step in script.split(", "):
        words = step.split(" ")
        apply(ds, words[0], words[1] if len(words) > 1 else "", counts, answers)
    print(f"{script} -> {', '.join(answers)}")


seed = 432


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    run("inc hello, inc hello, max, min, inc leet, max, min")
    run("max, min")
    run("inc a, dec a, max, min")
    run("inc a, inc b, inc b, inc c, inc c, inc c, max, min, dec c, dec c, max, min")
    run("inc a, inc a, inc a, dec a, dec a, max, min")
    run("inc x, inc y, inc z, max, min, inc y, max, min, dec y, dec y, max, min")
    run("inc a, inc a, inc a, inc b, dec a, max, min, dec a, max, min, dec b, max, min")
    ds = AllOne()
    counts = {}
    answers = []
    for _ in range(20000):
        roll = next_random() % 20
        key = f"k{next_random() % 50}"
        if roll < 4:
            apply(ds, "max", "", counts, answers)
        elif roll < 8:
            apply(ds, "min", "", counts, answers)
        elif roll < 13 and counts:
            start = next_random() % 50
            i = 0
            while True:
                k = f"k{(start + i) % 50}"
                if k in counts:
                    apply(ds, "dec", k, counts, answers)
                    break
                i += 1
        else:
            apply(ds, "inc", key, counts, answers)
    failed = 0
    checksum = 0
    for a in answers:
        if a.endswith(" FAILED"):
            failed += 1
        for b in a.encode():
            checksum = (checksum * 31 + b) % 1000000007
    total = sum(counts.values())
    print(f"20000 random operations on 50 keys: {len(answers)} queries, {failed} failed, {len(counts)} keys left, total count {total}, checksum {checksum}")


main()
