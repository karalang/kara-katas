# LeetCode #2254: Design Video Sharing Platform -- Python mirror of
# videos.kara: the videos in a list indexed by id (None once removed) and
# the freed ids in a min-heap; upload takes the smallest freed id, or a
# new slot at the end when none is free.
import heapq


class Video:
    def __init__(self, content):
        self.content = content
        self.views = 0
        self.likes = 0
        self.dislikes = 0


class Platform:
    def __init__(self):
        self.slots = []
        self.free = []

    def upload(self, video):
        held = Video(video)
        if self.free:
            vid = heapq.heappop(self.free)
            self.slots[vid] = held
            return vid
        self.slots.append(held)
        return len(self.slots) - 1

    def remove(self, vid):
        if vid < len(self.slots) and self.slots[vid] is not None:
            self.slots[vid] = None
            heapq.heappush(self.free, vid)

    def watch(self, vid, start, end):
        if vid >= len(self.slots) or self.slots[vid] is None:
            return "-1"
        video = self.slots[vid]
        video.views += 1
        last = min(end, len(video.content) - 1)
        return video.content[start:last + 1]

    def like(self, vid):
        if vid < len(self.slots) and self.slots[vid] is not None:
            self.slots[vid].likes += 1

    def dislike(self, vid):
        if vid < len(self.slots) and self.slots[vid] is not None:
            self.slots[vid].dislikes += 1

    def get_likes_and_dislikes(self, vid):
        if vid < len(self.slots) and self.slots[vid] is not None:
            return [self.slots[vid].likes, self.slots[vid].dislikes]
        return [-1]

    def get_views(self, vid):
        if vid < len(self.slots) and self.slots[vid] is not None:
            return self.slots[vid].views
        return -1


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def run(calls):
    platform = Platform()
    answers = []
    for kind, args, text in calls:
        if kind == 0:
            answers.append(str(platform.upload(text)))
        elif kind == 1:
            platform.remove(args[0])
        elif kind == 2:
            answers.append(platform.watch(args[0], args[1], args[2]))
        elif kind == 3:
            platform.like(args[0])
        elif kind == 4:
            platform.dislike(args[0])
        elif kind == 5:
            answers.append(show(platform.get_likes_and_dislikes(args[0])))
        else:
            answers.append(str(platform.get_views(args[0])))
    return answers


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def calls_of(count, longest):
    calls = []
    uploads = 0
    for _ in range(count):
        pick = next_random() % 10
        vid = next_random() % (uploads + 2)
        if pick < 3:
            length = next_random() % (longest - 2) + 3
            digits = "".join(str(next_random() % 10) for _ in range(length))
            calls.append((0, [], digits))
            uploads += 1
        elif pick == 3:
            calls.append((1, [vid], ""))
        elif pick < 6:
            start = next_random() % 3
            end = start + next_random() % 8 + 1
            calls.append((2, [vid, start, end], ""))
        else:
            calls.append((pick - 3, [vid], ""))
    return calls


def tally(answers, check):
    c = check
    for answer in answers:
        for b in answer.encode():
            c = (c * 131 + b) % 1000000007
        c = (c * 131 + 1) % 1000000007
    return c


def show_calls(calls):
    return "[" + ", ".join(f"({k}, {show(a)}, {t})" for k, a, t in calls) + "]"


def main():
    global seed
    examples = [
        [(0, [], "123"), (0, [], "456"), (1, [4], ""), (1, [0], ""), (0, [], "789"), (2, [1, 0, 5], ""), (2, [1, 0, 1], ""), (3, [1], ""), (4, [1], ""), (4, [1], ""), (5, [1], ""), (6, [1], "")],
        [(2, [0, 0, 1], ""), (3, [0], ""), (4, [0], ""), (5, [0], ""), (6, [0], "")],
        [(0, [], "1"), (0, [], "22"), (0, [], "333"), (0, [], "4444"), (1, [2], ""), (1, [0], ""), (0, [], "55"), (0, [], "66"), (0, [], "77"), (2, [2, 0, 9], "")],
        [(0, [], "0123456789"), (2, [0, 7, 100000], ""), (2, [0, 9, 10], ""), (2, [0, 0, 9], ""), (6, [0], "")],
        [(0, [], "42"), (1, [0], ""), (1, [0], ""), (5, [0], ""), (6, [0], ""), (0, [], "7"), (5, [0], "")],
        [(0, [], "900"), (3, [0], ""), (3, [0], ""), (4, [0], ""), (2, [0, 1, 2], ""), (1, [0], ""), (0, [], "8"), (5, [0], ""), (6, [0], ""), (2, [0, 0, 3], "")],
    ]
    for calls in examples:
        print(f"{show_calls(calls)} -> {show(run(calls))}")
    seed = 2254
    answered = 0
    check = 0
    for _ in range(3000):
        count = next_random() % 30 + 1
        answers = run(calls_of(count, 8))
        answered += len(answers)
        check = tally(answers, check)
    print(f"3000 small platforms: {answered} answers, checksum {check}")
    answered = 0
    check = 0
    for _ in range(4):
        answers = run(calls_of(25000, 8))
        answered += len(answers)
        check = tally(answers, check)
    print(f"4 large platforms: {answered} answers, checksum {check}")


main()
