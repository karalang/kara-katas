# Benchmark for #489: Python mirror of the ★ arm (backtracking); see
# robot_room_cleaner.kara.
import sys
import threading

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
        self.room = [line[:] for line in room]
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rooms = []
    starts = []
    seed = [489]
    for _ in range(300):
        room = [[0 if next_random(seed) % 4 == 0 else 1 for _ in range(100)] for _ in range(100)]
        row = next_random(seed) % 100
        col = next_random(seed) % 100
        room[row][col] = 1
        rooms.append(room)
        starts.append((row, col))
    total = 0
    checksum = 0
    for room, (row, col) in zip(rooms, starts):
        robot = Robot(room, row, col, 0)
        clean_room(robot)
        cleaned = 0
        for r in range(100):
            for c in range(100):
                if robot.cleaned[r][c] > 0:
                    cleaned += 1
                    checksum = (checksum * 31 + r * 100 + c) % 1000000007
        total += cleaned
        checksum = (checksum * 31 + robot.calls) % 1000000007
    print(f"300 rooms of 100 by 100: {total} cells cleaned, checksum {checksum}")


# The search recurses once per cell, up to 10,000 deep.
sys.setrecursionlimit(100000)
threading.stack_size(512 * 1024 * 1024)
thread = threading.Thread(target=main)
thread.start()
thread.join()
