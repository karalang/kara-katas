# LeetCode #2018: Check if Word Can Be Placed In Crossword -- Python mirror of
# the ★ arm (crossword.kara). Every row and every column is cut at its walls
# into runs; the word fits a run exactly as long as it whose every cell is
# empty or already holds the word's letter there, read forwards or backwards.


def fits(segment, word):
    k = len(word)
    if len(segment) != k:
        return False
    forward = all(segment[i] == ' ' or segment[i] == word[i] for i in range(k))
    backward = all(segment[i] == ' ' or segment[i] == word[k - 1 - i] for i in range(k))
    return forward or backward


def place_word_in_crossword(board, word):
    word = list(word)
    m, n = len(board), len(board[0])
    lines = [list(row) for row in board]
    for c in range(n):
        lines.append([board[r][c] for r in range(m)])
    for line in lines:
        segment = []
        for i in range(len(line) + 1):
            if i == len(line) or line[i] == '#':
                if fits(segment, word):
                    return True
                segment.clear()
            else:
                segment.append(line[i])
    return False


# ---- test harness ----------------------------------------------------------

seed = 2018


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_board(m, n, walls, filled, letters):
    board = []
    for _ in range(m):
        row = []
        for _ in range(n):
            if next_random() % 10 < walls:
                row.append('#')
            elif next_random() % 10 < filled:
                row.append(chr(ord('a') + next_random() % letters))
            else:
                row.append(' ')
        board.append(row)
    return board


def random_word(length, letters):
    return ''.join(chr(ord('a') + next_random() % letters) for _ in range(length))


def main():
    examples = [
        (["# #", "  #", "#c "], "abc"),
        ([" #a", " #c", " #a"], "ac"),
        (["# #", "  #", "# c"], "ca"),
        (["a"], "a"),
        ([" "], "ab"),
        (["#  #"], "ab"),
        (["  ", "  "], "ab"),
        (["#b#", "#a#", "# #"], "abc"),
        (["#####", "#   #", "#####"], "xyz"),
    ]
    for rows, word in examples:
        board = [list(r) for r in rows]
        answer = str(place_word_in_crossword(board, word)).lower()
        print(f"[{', '.join(rows)}], \"{word}\" -> {answer}")
    placed = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 6 + 1
        n = next_random() % 6 + 1
        walls = next_random() % 5
        filled = next_random() % 6
        letters = next_random() % 3 + 1
        length = next_random() % 5 + 1
        board = random_board(m, n, walls, filled, letters)
        word = random_word(length, letters)
        answer = place_word_in_crossword(board, word)
        placed += answer
        check = (check * 2 + int(answer)) % 1000000007
    print(f"3000 boards of up to 6 by 6: {placed} placed, checksum {check}")
    placed = 0
    check = 0
    for a in range(6):
        m = [300, 1, 400, 30, 600, 2][a]
        n = [300, 1000, 250, 3000, 150, 500][a]
        walls = [2, 3, 1, 4, 2, 0][a]
        length = [3, 5, 8, 2, 4, 500][a]
        board = random_board(m, n, walls, 1, 2)
        word = random_word(length, 2)
        answer = place_word_in_crossword(board, word)
        placed += answer
        check = (check * 2 + int(answer)) % 1000000007
    print(f"6 boards of up to 100000 cells: {placed} placed, checksum {check}")


main()
