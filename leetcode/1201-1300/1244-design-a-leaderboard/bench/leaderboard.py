# LeetCode #1244 bench, in Python: the ★ arm (each player's total in a
# dict; a top sorts the totals from the highest and adds the first k) on
# 100 sessions of 3000 random calls on players up to 10000; the tops'
# answers folded into a checksum.


class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player_id, score):
        self.scores[player_id] = self.scores.get(player_id, 0) + score

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])

    def reset(self, player_id):
        del self.scores[player_id]


seed = 1244


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def session(calls, players):
    board = Leaderboard()
    on = []
    check = 0
    tops = 0
    for _ in range(calls):
        op = next_random() % 4
        if op <= 1 or not on:
            player = next_random() % players + 1
            board.add_score(player, next_random() % 100 + 1)
            if player not in on:
                on.append(player)
        elif op == 2:
            got = board.top(next_random() % len(on) + 1)
            check = (check * 131 + got) % 1000000007
            tops += 1
        else:
            i = next_random() % len(on)
            on[i], on[-1] = on[-1], on[i]
            board.reset(on.pop())
    return tops, check


def main():
    tops = 0
    check = 0
    for _ in range(100):
        t, c = session(3000, 10000)
        tops += t
        check = (check * 31 + c) % 1000000007
    print(f"100 sessions of 3000 calls on 10000 players: {tops} tops, checksum {check}")


main()
