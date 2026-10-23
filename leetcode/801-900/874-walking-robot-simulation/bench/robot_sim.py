# LeetCode #874 bench: Python mirror of robot_sim.kara (the ★ arm, a set
# of obstacles) on the same 600 walks.


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


def main():
    command_lists = []
    obstacle_lists = []
    for k in range(20):
        command_lists.append(random_commands(10000, 2 + k % 3))
        obstacle_lists.append(random_obstacles(10000, 100 + 10 * k))
    total = 0
    check = 0
    for k in range(600):
        answer = robot_sim(command_lists[k % 20], obstacle_lists[(k * 7 + k // 20) % 20])
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"600 walks of 10000 commands among 10000 obstacles: distances sum to {total}, checksum {check}")


main()
