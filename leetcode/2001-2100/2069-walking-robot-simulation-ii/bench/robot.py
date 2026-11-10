# LeetCode #2069: Walking Robot Simulation II -- Python mirror of the ★
# arm's benchmark (robot.kara): 200 robots of 2 to 100 by 2 to 100, 50000
# calls each, half of them steps of up to 100000 cells.


class Robot:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.at = 0
        self.moved = False

    def step(self, num):
        self.moved = True
        self.at = (self.at + num) % (2 * (self.width + self.height) - 4)

    def get_pos(self):
        w, h, at = self.width - 1, self.height - 1, self.at
        if at <= w:
            return [at, 0]
        if at <= w + h:
            return [w, at - w]
        if at <= 2 * w + h:
            return [2 * w + h - at, h]
        return [0, 2 * w + 2 * h - at]

    def get_dir(self):
        w, h, at = self.width - 1, self.height - 1, self.at
        if at == 0:
            return "South" if self.moved else "East"
        if at <= w:
            return "East"
        if at <= w + h:
            return "North"
        if at <= 2 * w + h:
            return "West"
        return "South"


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2069]
    check = 0
    for t in range(200):
        robot = Robot(2 + t % 99, 2 + t * 7 % 99)
        for _ in range(50000):
            kind = next_random(seed) % 4
            if kind < 2:
                robot.step((next_random(seed) * 32768 + next_random(seed)) % 100000 + 1)
            elif kind == 2:
                p = robot.get_pos()
                check = (check * 31 + p[0] * 1000 + p[1]) % 1000000007
            else:
                check = (check * 31 + len(robot.get_dir())) % 1000000007
    print(f"200 robots, 10000000 calls: checksum {check}")


main()
