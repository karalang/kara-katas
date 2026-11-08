# LeetCode #1500: Design a File Sharing System -- the Python mirror of the
# ★ arm: each chunk's owners in a set read out sorted, each user's chunks in
# a list, the ids given back by leave in a min-heap.

import heapq


class FileSharing:
    def __init__(self, m):
        self.owners = {}
        self.owned = {}
        self.free = []
        self.next = 1

    def join(self, chunks):
        if self.free:
            uid = heapq.heappop(self.free)
        else:
            uid = self.next
            self.next += 1
        for c in chunks:
            self.owners.setdefault(c, set()).add(uid)
        self.owned[uid] = list(chunks)
        return uid

    def leave(self, uid):
        for c in self.owned.pop(uid, []):
            self.owners[c].discard(uid)
        heapq.heappush(self.free, uid)

    def request(self, uid, chunk):
        answer = sorted(self.owners.get(chunk, ()))
        if answer:
            s = self.owners.setdefault(chunk, set())
            if uid not in s:
                s.add(uid)
                self.owned[uid].append(chunk)
        return answer


seed = 1500


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_chunks(m, most):
    count = next_random() % (min(most, m) + 1)
    chunks = []
    while len(chunks) < count:
        c = next_random() % m + 1
        if c not in chunks:
            chunks.append(c)
    return chunks


def show(ids):
    return "[" + ", ".join(str(x) for x in ids) + "]"


def simulate(m, ops, most):
    system = FileSharing(m)
    live = []
    joins = requests = owners = check = 0
    for _ in range(ops):
        r = next_random() % 10
        if not live or r < 3:
            uid = system.join(random_chunks(m, most))
            live.append(uid)
            joins += 1
            check = mix(check, uid)
        elif r < 5:
            at = next_random() % len(live)
            live[at], live[-1] = live[-1], live[at]
            system.leave(live.pop())
        else:
            user = live[next_random() % len(live)]
            chunk = next_random() % m + 1
            answer = system.request(user, chunk)
            requests += 1
            owners += len(answer)
            check = mix(check, len(answer))
            for x in answer:
                check = mix(check, x)
    return joins, requests, owners, check


def batch(count, most_m, ops, most):
    joins = requests = owners = check = 0
    for _ in range(count):
        m = next_random() % most_m + 1
        j, r, o, c = simulate(m, ops, most)
        joins += j
        requests += r
        owners += o
        check = mix(check, c)
    print(f"{count} systems of up to {most_m} chunks, {ops} calls each: {joins} joins, "
          f"{requests} requests, {owners} owners returned, checksum {check}")


def main():
    system = FileSharing(4)
    a = system.join([1, 2])
    b = system.join([2, 3])
    c = system.join([4])
    r1 = system.request(1, 3)
    r2 = system.request(2, 2)
    system.leave(1)
    r3 = system.request(2, 1)
    system.leave(2)
    d = system.join([])
    print(f"join -> {a}, {b}, {c}; request(1, 3) -> {show(r1)}; request(2, 2) -> {show(r2)}; "
          f"leave(1); request(2, 1) -> {show(r3)}; leave(2); join -> {d}")
    batch(3000, 6, 40, 4)
    batch(300, 30, 300, 10)
    batch(10, 100000, 3000, 100)
    batch(4, 5, 5000, 5)


main()
