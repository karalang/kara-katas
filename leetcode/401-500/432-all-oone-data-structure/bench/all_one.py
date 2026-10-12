# Benchmark for #432: mirror of all_one.kara (a list of count buckets).
import sys


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


seed = 432


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    keys = 10000
    operations = int(sys.argv[1]) if len(sys.argv) > 1 else 2000000
    ds = AllOne()
    count = [0] * keys
    queries = 0
    checksum = 0
    for _ in range(operations):
        roll = next_random() % 10
        hi = next_random()
        key_id = (hi * 32768 + next_random()) % keys
        if roll < 2:
            answer = ds.get_max_key() if roll == 0 else ds.get_min_key()
            c = count[int(answer[1:])] if answer else 0
            queries += 1
            checksum = (checksum * 31 + c + 1) % 1000000007
        elif roll < 5 and count[key_id] > 0:
            ds.dec(f"k{key_id}")
            count[key_id] -= 1
        else:
            ds.inc(f"k{key_id}")
            count[key_id] += 1
    print(f"{operations} operations on {keys} keys: {queries} queries, checksum {checksum}")


main()
