"""LeetCode 253 - Meeting Rooms II. Python oracle.

Mirrors min_meeting_rooms.kara algorithm-for-algorithm: sort by start, keep a
min-heap of end times, release every room whose end has passed (`<=`, so a
meeting ending exactly now frees its room), and report the peak heap size.

The heap is hand-rolled rather than heapq, to mirror the .kara sift-up/sift-down
rather than delegating to a different implementation.
"""


def heap_push(heap, v):
    heap.append(v)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] < heap[parent]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break


def heap_pop(heap):
    n = len(heap)
    if n == 0:
        return
    last = heap.pop()
    if n == 1:
        return
    heap[0] = last
    m = len(heap)
    i = 0
    while True:
        l, r = 2 * i + 1, 2 * i + 2
        smallest = i
        if l < m and heap[l] < heap[smallest]:
            smallest = l
        if r < m and heap[r] < heap[smallest]:
            smallest = r
        if smallest == i:
            break
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest


def min_meeting_rooms(intervals):
    s = sorted(intervals, key=lambda x: x[0])
    heap = []
    rooms = 0
    for iv in s:
        while heap and heap[0] <= iv[0]:
            heap_pop(heap)
        heap_push(heap, iv[1])
        rooms = max(rooms, len(heap))
    return rooms


def main():
    cases = [
        ([(0, 30), (5, 10), (15, 20)], "[[0,30],[5,10],[15,20]]"),
        ([(7, 10), (2, 4)], "[[7,10],[2,4]]"),
        ([], "[]"),
        ([(1, 5)], "[[1,5]]"),
        ([(1, 5), (5, 10)], "[[1,5],[5,10]]"),
        ([(1, 10), (2, 3)], "[[1,10],[2,3]]"),
        ([(1, 3), (3, 5), (5, 7), (7, 9)], "[[1,3],[3,5],[5,7],[7,9]]"),
        ([(1, 4), (2, 5), (3, 6)], "[[1,4],[2,5],[3,6]]"),
        ([(1, 2), (1, 2), (1, 2)], "[[1,2],[1,2],[1,2]]"),
        ([(9, 10), (4, 9), (4, 17)], "[[9,10],[4,9],[4,17]]"),
        ([(2, 11), (6, 16), (11, 16)], "[[2,11],[6,16],[11,16]]"),
    ]
    for iv, label in cases:
        print(f"{label} -> {min_meeting_rooms(iv)}")


if __name__ == "__main__":
    main()
