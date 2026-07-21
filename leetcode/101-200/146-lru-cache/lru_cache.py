"""LeetCode 146 — LRU Cache (Python mirror / oracle).

Same index-based node-pool design as lru_cache.kara: pool[0]/pool[1] are the
head/tail sentinels, real nodes at 2+, prev/next are pool indices, and a dict
maps key -> pool index. O(1) get/put with LRU eviction.
"""


class DNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = 0
        self.next = 0


def main():
    cap = 2
    pool = [DNode(0, 0), DNode(0, 0)]  # 0 = head, 1 = tail
    pool[0].prev = 1
    pool[0].next = 1
    pool[1].prev = 0
    pool[1].next = 0
    m = {}
    size = 0

    def unlink(i):
        p, n = pool[i].prev, pool[i].next
        pool[p].next = n
        pool[n].prev = p

    def push_front(i):
        first = pool[0].next
        pool[i].prev = 0
        pool[i].next = first
        pool[first].prev = i
        pool[0].next = i

    def move_front(i):
        unlink(i)
        push_front(i)

    ops = [
        ("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3),
        ("get", 2, 0), ("put", 4, 4), ("get", 1, 0), ("get", 3, 0), ("get", 4, 0),
    ]
    for kind, key, val in ops:
        if kind == "get":
            if key in m:
                idx = m[key]
                move_front(idx)
                print(pool[idx].val)
            else:
                print(-1)
        else:
            if key in m:
                idx = m[key]
                pool[idx].val = val
                move_front(idx)
            else:
                pool.append(DNode(key, val))
                idx = len(pool) - 1
                m[key] = idx
                push_front(idx)
                size += 1
                if size > cap:
                    lru = pool[1].prev
                    del m[pool[lru].key]
                    unlink(lru)
                    size -= 1


main()
