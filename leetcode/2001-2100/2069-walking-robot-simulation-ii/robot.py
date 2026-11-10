# LeetCode #2069: Walking Robot Simulation II -- the Python mirror of
# robot.kara (the ★ arm): the robot kept as its place on the loop of the
# grid's edge, a step added modulo the loop's length.


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


def answers(width, height, calls):
    robot = Robot(width, height)
    out = []
    for call, num in calls:
        if call == 0:
            robot.step(num)
            out.append("null")
        elif call == 1:
            p = robot.get_pos()
            out.append(f"[{p[0]}, {p[1]}]")
        else:
            out.append(robot.get_dir())
    return out


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def calls_of(count, most, seed):
    calls = []
    for _ in range(count):
        kind = next_random(seed) % 4
        if kind < 2:
            calls.append((0, (next_random(seed) * 32768 + next_random(seed)) % most + 1))
        else:
            calls.append((kind - 1, 0))
    return calls


def checksum(answers):
    check = 0
    for a in answers:
        for b in a.encode():
            check = (check * 131 + b) % 1000000007
        check = (check * 131 + 10) % 1000000007
    return check


def main():
    example = [(0, 2), (0, 2), (1, 0), (2, 0), (0, 2), (0, 1), (0, 4), (1, 0), (2, 0)]
    print(f"6 x 3: {' '.join(answers(6, 3, example))}")
    round_ = [(2, 0), (0, 14), (1, 0), (2, 0), (0, 13), (1, 0), (2, 0), (0, 1), (1, 0), (2, 0)]
    print(f"5 x 4: {' '.join(answers(5, 4, round_))}")
    seed = [2069]
    check = 0
    for _ in range(300):
        width = next_random(seed) % 11 + 2
        height = next_random(seed) % 11 + 2
        count = next_random(seed) % 40 + 1
        most = [60, 100000][next_random(seed) % 2]
        calls = calls_of(count, most, seed)
        check = (check * 31 + checksum(answers(width, height, calls))) % 1000000007
    print(f"300 robots: checksum {check}")
    calls = calls_of(10000, 100000, seed)
    last = answers(100, 100, calls)
    print(f"100 x 100, 10000 calls: checksum {checksum(last)}, last {last[-2]} {last[-1]}")


if __name__ == "__main__":
    main()
