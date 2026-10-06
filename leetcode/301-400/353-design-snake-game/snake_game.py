# LeetCode #353: Design Snake Game -- Python mirror of snake_game.kara.
# A deque of body cells plus a set of the cells it covers; cells are
# row * width + col, head last.
from collections import deque


class SnakeGame:
    def __init__(self, width, height, food):
        self.width, self.height, self.food = width, height, food
        self.next_food = 0
        self.body = deque([0])
        self.covered = {0}

    def step(self, d):
        head = self.body[-1]
        r, c = head // self.width, head % self.width
        nr, nc = {'U': (r - 1, c), 'D': (r + 1, c), 'L': (r, c - 1)}.get(d, (r, c + 1))
        if nr < 0 or nr >= self.height or nc < 0 or nc >= self.width:
            return -1
        cell = nr * self.width + nc
        if self.next_food < len(self.food) and self.food[self.next_food] == (nr, nc):
            self.next_food += 1
        else:
            self.covered.discard(self.body.popleft())
        if cell in self.covered:
            return -1
        self.body.append(cell)
        self.covered.add(cell)
        return self.next_food


def cycle_moves(width, height):
    m = ['R'] * (width - 1)
    for row in range(1, height):
        m.append('D')
        m += ['L' if row % 2 == 1 else 'R'] * (width - 2)
    m.append('L')
    m += ['U'] * (height - 1)
    return ''.join(m)


def play(label, width, height, food, moves):
    g = SnakeGame(width, height, food)
    out = []
    for d in moves:
        s = g.step(d)
        out.append(f" {s}")
        if s < 0:
            break
    print(f"{label}:{''.join(out)}")


play("example", 3, 2, [(1, 2), (0, 1)], "RDRULU")
play("wall", 2, 2, [], "U")
play("tail chase", 2, 2, [(0, 1), (1, 1)], "RDLURDLURD")
play("self bite", 3, 3, [(0, 1), (0, 2), (1, 2), (1, 1)], "RRDLU")
play("no food left", 4, 1, [(0, 1)], "RRRLL")
play("turn back at length 2", 3, 1, [(0, 1)], "RL")
play("turn back at length 3", 3, 1, [(0, 1), (0, 2)], "RRL")

w, h = 60, 40
cells = cycle_moves(w, h)
n = len(cells)
pos = []
r = c = 0
for d in cells:
    if d == 'U':
        r -= 1
    elif d == 'D':
        r += 1
    elif d == 'L':
        c -= 1
    else:
        c += 1
    pos.append((r, c))
food = [pos[(3 * i + 2) % n] for i in range(1000)]
g = SnakeGame(w, h, food)
checksum = 0
total = 3 * n
for t in range(total):
    s = g.step(cells[t % n])
    checksum = (checksum * 31 + s + t) % 1000000007
    if (t + 1) % 1200 == 0:
        print(f"after {t + 1} moves: score {s}, length {len(g.body)}")
print(f"bite: {g.step('D')}")
print(f"long game: {total} moves, checksum {checksum}")
