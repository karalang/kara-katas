# LeetCode #2018: Check if Word Can Be Placed In Crossword -- the ★ arm's
# benchmark, a mirror of crossword.kara.


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


seed = 2018


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    boards = []
    words = []
    for b in range(120):
        walls = b % 2 + 1
        board = []
        for _ in range(200):
            row = []
            for _ in range(200):
                if next_random() % 10 < walls:
                    row.append('#')
                elif next_random() % 10 < 4:
                    row.append(chr(ord('a') + next_random() % 3))
                else:
                    row.append(' ')
            board.append(row)
        word = ''.join(chr(ord('a') + next_random() % 3) for _ in range(b % 10 + 10))
        boards.append(board)
        words.append(word)
    calls = placed = check = 0
    for _ in range(40):
        for b in range(len(boards)):
            answer = place_word_in_crossword(boards[b], words[b])
            calls += 1
            placed += answer
            check = (check * 2 + int(answer)) % 1000000007
    print(f"{calls} calls: {placed} placed, checksum {check}")


main()
