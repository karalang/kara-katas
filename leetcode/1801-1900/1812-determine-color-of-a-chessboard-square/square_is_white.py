# LeetCode #1812: Determine Color of a Chessboard Square -- the ★ arm in
# Python: a square is white exactly when its file and rank, counted from a
# and 1, sum to an odd number.


def square_is_white(coordinates):
    file = ord(coordinates[0]) - ord("a")
    rank = ord(coordinates[1]) - ord("1")
    return (file + rank) % 2 == 1


def show(b):
    return "true" if b else "false"


def main():
    # LeetCode's three examples
    print(*[show(square_is_white(c)) for c in ["a1", "h3", "c7"]])
    # the edges
    print(*[show(square_is_white(c)) for c in ["a8", "h1", "h8", "b1"]])
    # every square
    whites = 0
    for rank in range(8, 0, -1):
        row = ""
        for file in "abcdefgh":
            if square_is_white(f"{file}{rank}"):
                row += "W"
                whites += 1
            else:
                row += "B"
        print(row)
    print(f"{whites} white squares")


main()
