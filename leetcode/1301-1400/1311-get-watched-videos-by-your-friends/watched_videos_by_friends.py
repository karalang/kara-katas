# LeetCode #1311: Get Watched Videos by Your Friends -- Python mirror of the
# ★ arm: a breadth-first walk a level at a time, the videos of the people
# left counted, then sorted as (count, title) pairs.


def watched_videos_by_friends(watched_videos, friends, id, level):
    seen = [False] * len(friends)
    seen[id] = True
    people = [id]
    for _ in range(level):
        nxt = []
        for p in people:
            for f in friends[p]:
                if not seen[f]:
                    seen[f] = True
                    nxt.append(f)
        people = nxt
    count = {}
    for p in people:
        for video in watched_videos[p]:
            count[video] = count.get(video, 0) + 1
    return [video for _, video in sorted((c, video) for video, c in count.items())]


seed = 1311


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return ",".join(v) if v else "-"


def ask(watched, friends, id, level):
    return show(watched_videos_by_friends(watched, friends, id, level))


def main():
    square = [[1, 2], [0, 3], [0, 3], [1, 2]]
    e1 = ask([["A", "B"], ["C"], ["B", "C"], ["D"]], square, 0, 1)
    e2 = ask([["A", "B"], ["C"], ["B", "C"], ["D"]], square, 0, 2)
    past = ask([["a"], ["b"], ["c"]], [[1], [0], []], 0, 2)
    triangle = ask([["x"], ["y"], ["z"], ["w"]], [[1, 2], [0, 2], [0, 1, 3], [2]], 0, 2)
    tie = ask([[], ["bb", "ab"], ["ab", "bb", "c"]], [[1, 2], [0], [0]], 0, 1)
    twice = ask([[], ["m", "m", "k"], ["k", "j"]], [[1, 2], [0], [0]], 0, 1)
    print(f"{e1} {e2} {past} {triangle} {tie} {twice}")
    total = 0
    check = 0
    for g in range(600):
        n = 2 + next_random() % 39
        odds = 2 + next_random() % 11
        pool = 3 if g % 3 == 0 else 12 if g % 3 == 1 else 60
        titles = []
        for t in range(pool):
            title = ""
            k = t
            while True:
                title += "abcdefgh"[k % 8]
                k //= 8
                if k == 0:
                    break
            titles.append(title)
        friends = [[] for _ in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                if next_random() % odds == 0:
                    friends[a].append(b)
                    friends[b].append(a)
        watched = []
        for _ in range(n):
            videos = []
            for _ in range(next_random() % 7):
                videos.append(titles[next_random() % pool])
            watched.append(videos)
        id = next_random() % n
        if next_random() % 4 == 0:
            level = 1 + next_random() % (n - 1)
        else:
            level = 1 + next_random() % 3 % (n - 1)
        got = watched_videos_by_friends(watched, friends, id, level)
        total += len(got)
        for video in got:
            for c in video:
                check = (check * 31 + ord(c)) % 1000000007
            check = (check * 31 + 1) % 1000000007
        check = (check * 31 + 2) % 1000000007
    print(f"600 random groups: {total} videos, checksum {check}")


main()
