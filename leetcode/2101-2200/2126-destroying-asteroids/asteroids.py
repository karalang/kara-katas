# LeetCode #2126: Destroying Asteroids -- the mirror of asteroids.kara:
# the asteroids sorted, each destroyed in turn until one is too heavy.


def asteroids_destroyed(mass, asteroids):
    planet = mass
    for a in sorted(asteroids):
        if planet < a:
            return False
        planet += a
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(mass, asteroids):
    answer = "true" if asteroids_destroyed(mass, asteroids) else "false"
    print(f"mass {mass}, [{', '.join(map(str, asteroids))}] -> {answer}")


def main():
    show(10, [3, 9, 19, 5, 21])
    show(5, [4, 9, 23, 4])
    show(1, [1])
    show(1, [2])
    show(1, [8, 4, 2, 1])
    show(1, [9, 4, 2, 1])
    seed = [2126]
    destroyed = 0
    check = 0
    for rnd in range(3000):
        mass = next_random(seed) % 20 + 1
        n = next_random(seed) % 12 + 1
        top = [10, 30, 100][rnd % 3]
        asteroids = [next_random(seed) % top + 1 for _ in range(n)]
        if asteroids_destroyed(mass, asteroids):
            destroyed += 1
            check = (check * 31 + rnd) % 1000000007
    print(f"3000 cases: {destroyed} destroyed, checksum {check}")
    ladder = list(range(1, 100001))
    for i in range(len(ladder)):
        j = (next_random(seed) * 32768 + next_random(seed)) % len(ladder)
        ladder[i], ladder[j] = ladder[j], ladder[i]
    heavy = [100000] * 100000
    a = "true" if asteroids_destroyed(1, ladder) else "false"
    b = "true" if asteroids_destroyed(99999, heavy) else "false"
    c = "true" if asteroids_destroyed(100000, heavy) else "false"
    print(f"100000 asteroids: {a} from 1, {b} from 99999, {c} from 100000")


main()
