# LeetCode #1812: Determine Color of a Chessboard Square -- the bench in
# Python: the ★ arm over 3 * 10^7 calls, each of the 64 square names built
# once and drawn from the checksum so far.


def square_is_white(coordinates):
    file = ord(coordinates[0]) - ord("a")
    rank = ord(coordinates[1]) - ord("1")
    return (file + rank) % 2 == 1


def main():
    names = [f"{file}{rank}" for file in "abcdefgh" for rank in range(1, 9)]
    check = 0
    for call in range(30000000):
        name = names[(check + call) % 64]
        check = (check * 3 + (1 if square_is_white(name) else 2)) % 1000000007
    print(f"30000000 calls: checksum {check}")


main()
