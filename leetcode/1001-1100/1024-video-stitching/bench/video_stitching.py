# LeetCode #1024: Video Stitching -- bench
# Mirrors ./video_stitching.kara; see ../README.md § Benchmarks.


def video_stitching(clips, time):
    furthest = [0] * (time + 1)
    for clip in clips:
        if clip[0] <= time:
            furthest[clip[0]] = max(furthest[clip[0]], clip[1])
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 2000
    rounds = 500
    seed = [1024]
    cases = []
    total_clips = 0
    for _ in range(count):
        time = 50 + next_random(seed) % 51
        clips = []
        at = 0
        while at < time:
            length = 1 + next_random(seed) % 10
            back = next_random(seed) % 3
            clips.append([max(at - back, 0), min(at + length, 100)])
            at += length
        for _ in range(next_random(seed) % (101 - len(clips))):
            start = next_random(seed) % (time + 1)
            end = min(start + next_random(seed) % 21, 100)
            place = next_random(seed) % (len(clips) + 1)
            clips.insert(place, [start, end])
        total_clips += len(clips)
        cases.append((clips, time))
    total = 0
    check = 0
    for _ in range(rounds):
        for clips, time in cases:
            answer = video_stitching(clips, time)
            total += answer
            check = (check * 131 + answer + 1) % 1000000007
    print(f"{count} cases, {total_clips} clips, {rounds} rounds: sum {total}, checksum {check}")


main()
