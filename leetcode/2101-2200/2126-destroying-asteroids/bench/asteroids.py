# LeetCode #2126: Destroying Asteroids -- the benchmark, the same
# algorithm as asteroids.kara.


def asteroids_destroyed(mass, asteroids):
    planet = mass
    for a in sorted(asteroids):
        if planet < a:
            return False
        planet += a
    return True


def main():
    seed = 2126

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(20):
        arrays.append([(next_random() * 32768 + next_random()) % 99001 + 1000 for _ in range(100000)])
    destroyed = 0
    check = 0
    for rnd in range(10):
        for k in range(20):
            at = (next_random() * 32768 + next_random()) % 100000
            arrays[k][at] = next_random() % 2000 + 1
            mass = next_random() % 1000 + 500
            if asteroids_destroyed(mass, arrays[k]):
                destroyed += 1
                check = (check * 31 + rnd * 20 + k) % 1000000007
    print(f"200 solves: {destroyed} destroyed, checksum {check}")


main()
