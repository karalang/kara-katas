# LeetCode #1246: Palindrome Removal -- mirrors palindrome_removal.kara.


def minimum_moves(arr):
    n = len(arr)
    best = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            moves = 1 + best[i + 1][j]
            if i + 1 < j and arr[i + 1] == arr[i]:
                moves = min(moves, 1 + best[i + 2][j])
            for k in range(i + 2, j):
                if arr[k] == arr[i]:
                    moves = min(moves, best[i + 1][k] + best[k + 1][j])
            best[i][j] = moves
    return best[0][n]


seed = 1246


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{minimum_moves([1, 2])} {minimum_moves([1, 3, 4, 1, 5])}")
    total = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 100 + 1
        values = next_random() % 20 + 1
        arr = [next_random() % values + 1 for _ in range(n)]
        moves = minimum_moves(arr)
        total += moves
        check = (check * 131 + moves) % 1000000007
    print(f"1000 random arrays: total {total}, checksum {check}")
    wide = [next_random() % 20 + 1 for _ in range(100)]
    narrow = [next_random() % 2 + 1 for _ in range(100)]
    hill = [i + 1 if i < 50 else 100 - i for i in range(100)]
    print(f"100 values: from 1 to 20 {minimum_moves(wide)}, from 1 to 2 {minimum_moves(narrow)}, a hill {minimum_moves(hill)}")


main()
