# Bench mirror of snake_game.kara (the grid + ring-buffer arm), same algorithm.
ROUNDS, WIDTH, HEIGHT = 30, 1000, 400


class SnakeGame:
    def __init__(self, width, height, food):
        cap = width * height
        self.width, self.height, self.food = width, height, food
        self.next_food = 0
        self.ring = [0] * cap
        self.start, self.len = 0, 1
        self.covered = bytearray(cap)
        self.covered[0] = 1

    def step(self, d):
        cap = len(self.ring)
        head = self.ring[(self.start + self.len - 1) % cap]
        r, c = divmod(head, self.width)
        if d == 'U':
            r -= 1
        elif d == 'D':
            r += 1
        elif d == 'L':
            c -= 1
        else:
            c += 1
        if r < 0 or r >= self.height or c < 0 or c >= self.width:
            return -1
        cell = r * self.width + c
        if self.next_food < len(self.food) and self.food[self.next_food] == (r, c):
            self.next_food += 1
        else:
            self.covered[self.ring[self.start]] = 0
            self.start = (self.start + 1) % cap
            self.len -= 1
        if self.covered[cell]:
            return -1
        self.ring[(self.start + self.len) % cap] = cell
        self.len += 1
        self.covered[cell] = 1
        return self.next_food


def main():
    sink = 0
    for rnd in range(ROUNDS):
        w, h = WIDTH, HEIGHT + 2 * rnd
        n = w * h
        moves = ['R'] * (w - 1)
        for row in range(1, h):
            moves.append('D')
            moves += ['L' if row % 2 == 1 else 'R'] * (w - 2)
        moves.append('L')
        moves += ['U'] * (h - 1)
        food, r, c, t = [], 0, 0, 0
        while len(food) < n // 4:
            d = moves[t]
            if d == 'U':
                r -= 1
            elif d == 'D':
                r += 1
            elif d == 'L':
                c -= 1
            else:
                c += 1
            if t % 3 == 2:
                food.append((r, c))
            t += 1
        g = SnakeGame(w, h, food)
        for t in range(3 * n):
            s = g.step(moves[t % n])
            sink = (sink * 31 + s + t) % 1000000007
        sink = (sink + g.len) % 1000000007
    print(sink)


main()
