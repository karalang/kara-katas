# Benchmark for #406: mirror of queue_reconstruction.kara (tallest first,
# each inserted at its k).


def reconstruct_queue(people):
    order = sorted(people, key=lambda p: (-p[0], p[1]))
    queue = []
    for p in order:
        queue.insert(p[1], p)
    return queue


def main():
    queues = 1000
    n = 2000
    seed = 406
    rebuilt = 0
    checksum = 0

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    for _ in range(queues):
        count = [0] * 51
        line = []
        for _ in range(n):
            h = 1 + step() % 50
            k = 0
            for g in range(h, 51):
                k += count[g]
            count[h] += 1
            line.append((h, k))
        people = list(line)
        for i in range(n - 1, 0, -1):
            j = step() % (i + 1)
            people[i], people[j] = people[j], people[i]
        q = reconstruct_queue(people)
        if q == line:
            rebuilt += 1
        for h, k in q:
            checksum = (checksum * 31 + h * 10000 + k) % 1000000007
    print(f"{queues} queues of {n} people: {rebuilt} rebuilt, checksum {checksum}")


main()
