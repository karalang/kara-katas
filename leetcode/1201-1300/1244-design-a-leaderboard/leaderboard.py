# LeetCode #1244: Design A Leaderboard -- mirrors leaderboard.kara.


class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player_id, score):
        self.scores[player_id] = self.scores.get(player_id, 0) + score

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])

    def reset(self, player_id):
        del self.scores[player_id]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def session(calls, players, rng):
    board = Leaderboard()
    on = []
    check = 0
    tops = 0
    for _ in range(calls):
        op = rng.next() % 4
        if op <= 1 or not on:
            player = rng.next() % players + 1
            board.add_score(player, rng.next() % 100 + 1)
            if player not in on:
                on.append(player)
        elif op == 2:
            got = board.top(rng.next() % len(on) + 1)
            check = (check * 131 + got) % 1000000007
            tops += 1
        else:
            i = rng.next() % len(on)
            on[i], on[-1] = on[-1], on[i]
            board.reset(on.pop())
    return tops, check


def main():
    board = Leaderboard()
    for player, score in [(1, 73), (2, 56), (3, 39), (4, 51), (5, 4)]:
        board.add_score(player, score)
    first = board.top(1)
    board.reset(1)
    board.reset(2)
    board.add_score(2, 51)
    print(f"{first} {board.top(3)}")
    rng = Rng(1244)
    tops = 0
    check = 0
    for _ in range(1000):
        calls = rng.next() % 300 + 1
        players = rng.next() % 50 + 1
        t, c = session(calls, players, rng)
        tops += t
        check = (check * 31 + c) % 1000000007
    print(f"1000 sessions: {tops} tops, checksum {check}")
    t, c = session(3000, 10000, rng)
    print(f"3000 calls on 10000 players: {t} tops, checksum {c}")


main()
