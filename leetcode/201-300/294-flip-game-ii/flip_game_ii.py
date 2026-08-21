"""Oracle mirror for LeetCode 294 — same algorithm as flip_game_ii.kara.

Memoized backtracking: a position is winning exactly when some move leads to a
position that is losing for the opponent.
"""


def next_states(s):
    return [s[:i] + "--" + s[i + 2:]
            for i in range(len(s) - 1)
            if s[i] == "+" and s[i + 1] == "+"]


def can_win(s, memo):
    if s in memo:
        return memo[s]
    for t in next_states(s):
        if not can_win(t, memo):
            memo[s] = True
            return True
    memo[s] = False
    return False


def first_player_wins(s):
    return can_win(s, {})


def main():
    for s in ["++++", "+++++", "+", "-", "", "++", "+++",
              "+-+-+", "++-++", "++-+", "+++-+++", "++++++", "-++-++-++-"]:
        print(f"{s} -> {str(first_player_wins(s)).lower()}")


if __name__ == "__main__":
    main()
