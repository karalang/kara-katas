# LeetCode #874: Walking Robot Simulation -- Python mirror of the ★ arm (the
# robot walked one square at a time against a set of obstacles) and its
# test harness; prints the same output as robot_sim.kara.


def robot_sim(commands, obstacles):
    blocked = set(square(o[0], o[1]) for o in obstacles)
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    facing = 0
    x = 0
    y = 0
    best = 0
    for c in commands:
        if c == -2:
            facing = (facing + 3) % 4
        elif c == -1:
            facing = (facing + 1) % 4
        else:
            for _ in range(c):
                nx = x + dx[facing]
                ny = y + dy[facing]
                if square(nx, ny) in blocked:
                    break
                x = nx
                y = ny
                best = max(best, x * x + y * y)
    return best


def square(x, y):
    return (x + 200000) * 400001 + (y + 200000)


# ---- test harness ----------------------------------------------------------

seed = 874


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_commands(n, turns):
    commands = []
    for _ in range(n):
        if next_random() % turns == 0:
            commands.append(-1 - next_random() % 2)
        else:
            commands.append(next_random() % 9 + 1)
    return commands


def random_obstacles(n, reach):
    obstacles = []
    for _ in range(n):
        x = next_random() % (2 * reach + 1) - reach
        y = next_random() % (2 * reach + 1) - reach
        obstacles.append([x, y])
    return obstacles


def show(commands, obstacles):
    text = ",".join(str(c) for c in commands)
    otext = ",".join(f"[{o[0]},{o[1]}]" for o in obstacles)
    print(f"commands = [{text}], obstacles = [{otext}] -> {robot_sim(commands, obstacles)}")


def main():
    show([4, -1, 3], [])
    show([4, -1, 4, -2, 4], [[2, 4]])
    show([6, -1, -1, 6], [[0, 0]])
    show([-2, -2, -1, -1], [[1, 1]])
    show([5], [[0, 1]])
    show([-2, 9, -2, 9], [[-9, -5]])
    show([-1, -1, 7, -1, 3], [[0, -3], [-2, -7]])
    show([2, -1, 2, -1, 2, -1, 2, -1, 9], [[0, 5]])
    show([9, 9, 9, -1, 9, 9, 9], [[30000, 27], [0, 28], [0, -30000]])
    show([1, -1, 1, -1, 1, -1, 1], [[0, 0]])
    total = 0
    zero = 0
    for k in range(3000):
        commands = random_commands(k % 10 + 1, 3)
        obstacles = random_obstacles(k % 12, 5)
        answer = robot_sim(commands, obstacles)
        total += answer
        if answer == 0:
            zero += 1
    print(f"3000 walks of 1 to 10 commands: distances sum to {total}, {zero} never leaving the origin")
    check = 0
    total = 0
    for k in range(12):
        reach = 150 + 50 * k if k % 2 == 0 else 30000
        commands = random_commands(10000, 2 + k % 3)
        obstacles = random_obstacles(10000, reach)
        answer = robot_sim(commands, obstacles)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"12 walks of 10000 commands among 10000 obstacles: distances sum to {total}, checksum {check}")


main()
