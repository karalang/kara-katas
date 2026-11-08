# LeetCode #1500: Design a File Sharing System -- the benchmark, the same
# structure as bench/files.kara: each chunk's owners in a sorted list kept by
# bisect, each user's chunks in a list indexed by id, free ids in a min-heap.

import heapq
from bisect import bisect_left


class FileSharing:
    def __init__(self, m):
        self.owners = [[] for _ in range(m + 1)]
        self.owned = [[]]
        self.free = []

    def join(self, chunks):
        if self.free:
            uid = heapq.heappop(self.free)
        else:
            self.owned.append([])
            uid = len(self.owned) - 1
        for c in chunks:
            o = self.owners[c]
            o.insert(bisect_left(o, uid), uid)
        self.owned[uid] = chunks
        return uid

    def leave(self, uid):
        for c in self.owned[uid]:
            o = self.owners[c]
            del o[bisect_left(o, uid)]
        self.owned[uid] = []
        heapq.heappush(self.free, uid)

    def request(self, uid, chunk):
        o = self.owners[chunk]
        answer = list(o)
        if answer:
            at = bisect_left(o, uid)
            if at == len(o) or o[at] != uid:
                o.insert(at, uid)
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
    batch(40, 2000, 40000, 30)


main()
