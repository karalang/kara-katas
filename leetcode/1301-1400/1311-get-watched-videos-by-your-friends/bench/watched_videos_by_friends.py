# LeetCode #1311 bench, Python: the ★ arm (a breadth-first walk a level at a
# time, the videos of the people left counted in a dict, then sorted as
# (count, title) pairs) on the same 50 groups and 200 passes.


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


def fold(check, title):
    for ch in title:
        check = (check * 31 + ord(ch)) % 1000000007
    return check


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    titles = []
    for _ in range(400):
        length = 1 + next_random() % 8
        titles.append("".join(letters[next_random() % 26] for _ in range(length)))
    n = 100
    groups = []
    links = []
    for _ in range(50):
        friends = [[] for _ in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                if next_random() % 25 == 0:
                    friends[a].append(b)
                    friends[b].append(a)
        watched = [[titles[next_random() % 400] for _ in range(100)] for _ in range(n)]
        groups.append(watched)
        links.append(friends)
    check = 0
    for p in range(200):
        for g in range(50):
            groups[g][check % n][(check // 7) % 100] = titles[(check // 11) % 400]
            id = (check // 13) % n
            level = 1 + (check // 17) % 3
            got = watched_videos_by_friends(groups[g], links[g], id, level)
            check = (check * 31 + len(got)) % 1000000007
            if got:
                check = fold(check, got[0])
                check = fold(check, got[-1])
            check = (check + p) % 1000000007
    print(f"200 passes over 50 groups of 100: checksum {check}")


main()
