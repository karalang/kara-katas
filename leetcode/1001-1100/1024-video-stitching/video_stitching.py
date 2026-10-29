# LeetCode #1024: Video Stitching -- a greedy jump
# Mirrors video_stitching.kara (the ★ arm) and prints the same output.


def video_stitching(clips, time):
    furthest = [0] * (time + 1)
    for start, end in clips:
        if start <= time:
            furthest[start] = max(furthest[start], end)
    taken = 0
    covered = 0
    reach = 0
    for t in range(time):
        reach = max(reach, furthest[t])
        if reach <= t:
            return -1
        if t == covered:
            taken += 1
            covered = reach
    return taken


seed = 1024


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    examples = [
        ([[0, 2], [4, 6], [8, 10], [1, 9], [1, 5], [5, 9]], 10),
        ([[0, 1], [1, 2]], 5),
        ([[0, 1], [6, 8], [0, 2], [5, 6], [0, 4], [0, 3], [6, 7], [1, 3], [4, 7], [1, 4], [2, 5], [2, 6], [3, 4], [4, 5], [5, 7], [6, 9]], 9),
        ([[0, 4], [2, 8]], 5),
        ([[0, 5], [0, 5], [5, 10]], 10),
        ([[1, 5], [0, 1]], 5),
        ([[0, 3], [4, 6]], 6),
        ([[0, 0], [0, 100]], 100),
    ]
    for clips, time in examples:
        print(f"{clips}, time {time} -> {video_stitching(clips, time)}")
    groups = [(3000, 4, 6, 10), (2000, 10, 20, 20), (1000, 30, 50, 40), (500, 100, 100, 100), (500, 100, 30, 100), (300, 60, 100, 100)]
    for cases, count, longest, top in groups:
        total = 0
        none = 0
        check = 0
        for _ in range(cases):
            time = 1 + next_random() % top
            clips = []
            for _ in range(count):
                start = next_random() % (time + 1)
                end = min(start + next_random() % (longest + 1), 100)
                clips.append([start, end])
            answer = video_stitching(clips, time)
            if answer < 0:
                none += 1
            else:
                total += answer
            check = (check * 131 + answer + 1) % 1000000007
        print(f"{cases} cases of {count} clips (up to {longest} long, time up to {top}): {total} clips used, {none} impossible, checksum {check}")


main()
