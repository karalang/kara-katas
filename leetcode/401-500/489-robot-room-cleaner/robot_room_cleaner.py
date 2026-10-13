# LeetCode #489: Robot Room Cleaner -- backtracking.
# Mirrors robot_room_cleaner.kara (the ★ arm).
import sys

sys.setrecursionlimit(10000)

STEP = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def explore(robot, row, col, facing, visited):
    visited.add((row, col))
    robot.clean()
    d = facing
    for _ in range(4):
        nxt = (row + STEP[d][0], col + STEP[d][1])
        if nxt not in visited and robot.forward():
            explore(robot, nxt[0], nxt[1], d, visited)
            robot.turn_right()
            robot.turn_right()
            robot.forward()
            robot.turn_right()
            robot.turn_right()
        robot.turn_right()
        d = (d + 1) % 4


def clean_room(robot):
    explore(robot, 0, 0, 0, set())


class Robot:
    def __init__(self, room, row, col, facing):
        self.room = room
        self.row = row
        self.col = col
        self.facing = facing
        self.cleaned = [[0] * len(line) for line in room]
        self.calls = 0
        cells = len(room) * len(room[0])
        self.budget = 16 * cells * cells + 1000

    def forward(self):
        self.calls += 1
        if self.calls > self.budget:
            return False
        dr, dc = STEP[self.facing]
        r, c = self.row + dr, self.col + dc
        if r < 0 or r >= len(self.room) or c < 0 or c >= len(self.room[0]) or self.room[r][c] == 0:
            return False
        self.row, self.col = r, c
        return True

    def turn_left(self):
        self.calls += 1
        if self.calls <= self.budget:
            self.facing = (self.facing + 3) % 4

    def turn_right(self):
        self.calls += 1
        if self.calls <= self.budget:
            self.facing = (self.facing + 1) % 4

    def clean(self):
        self.calls += 1
        if self.calls <= self.budget:
            self.cleaned[self.row][self.col] += 1


def reachable(room, row, col):
    seen = [[0] * len(line) for line in room]
    stack = [(row, col)]
    seen[row][col] = 1
    while stack:
        r, c = stack.pop()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(room) and 0 <= nc < len(room[0]) and room[nr][nc] == 1 and seen[nr][nc] == 0:
                seen[nr][nc] = 1
                stack.append((nr, nc))
    return seen


def run(room, row, col):
    robot = Robot(room, row, col, 0)
    clean_room(robot)
    want = reachable(room, row, col)
    count = sum(1 for line in robot.cleaned for x in line if x > 0)
    right = robot.cleaned == want
    return count, right


def show(name, room, row, col):
    count, right = run(room, row, col)
    print(f"{name}: {count} cells cleaned, all and only the reachable ones once each: {'true' if right else 'false'}")


seed = 489


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("LeetCode", [
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ], 1, 3)
    show("one cell", [[1]], 0, 0)
    show("a corridor", [[1, 1, 1, 1, 1, 1, 1]], 0, 3)
    show("a closed-off corner", [
        [1, 1, 0, 1],
        [1, 1, 0, 1],
        [0, 0, 1, 1],
    ], 0, 0)
    show("a spiral", [
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ], 2, 2)
    show("an open room", [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ], 2, 0)
    count = 300
    total = 0
    right_rooms = 0
    checksum = 0
    for k in range(count):
        odds = 20 if k % 3 == 0 else 33 if k % 3 == 1 else 50
        rows = 1 + next_random() % 8
        cols = 1 + next_random() % 8
        room = [[0 if next_random() % 100 < odds else 1 for _ in range(cols)] for _ in range(rows)]
        row = next_random() % rows
        col = next_random() % cols
        room[row][col] = 1
        cleaned, right = run(room, row, col)
        total += cleaned
        if right:
            right_rooms += 1
        checksum = (checksum * 31 + cleaned * 7 + rows * cols) % 1000000007
    print(f"{count} random rooms: {total} cells cleaned, {right_rooms} rooms cleaned right, checksum {checksum}")


main()
