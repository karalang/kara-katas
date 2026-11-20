# LeetCode #2383: Minimum Hours of Training to Win a Competition -- the
# Python mirror of training.kara.


def min_number_of_hours(initial_energy, initial_experience, energy, experience):
    needed = sum(energy) + 1
    hours = 0
    if initial_energy < needed:
        hours = needed - initial_energy
    have = initial_experience
    for e in experience:
        if have <= e:
            hours += e + 1 - have
            have = e + 1
        have += e
    return hours


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536



def main():
    global seed
    print(min_number_of_hours(5, 3, [1, 4, 3, 2], [2, 6, 3, 1]))
    print(min_number_of_hours(2, 4, [1], [3]))
    print(min_number_of_hours(3, 3, [3], [3]))
    strong = [100] * 100
    print(f"{min_number_of_hours(1, 1, strong, strong)} {min_number_of_hours(100, 100, strong, strong)}")
    seed = 2383
    check = 0
    total = 0
    none = 0
    for _ in range(3000):
        n = 1 + next_random() % 100
        top = 1 + next_random() % 100
        initial_energy = 1 + next_random() % 100
        initial_experience = 1 + next_random() % 100
        energy = [1 + next_random() % top for _ in range(n)]
        experience = [1 + next_random() % top for _ in range(n)]
        hours = min_number_of_hours(initial_energy, initial_experience, energy, experience)
        check = (check * 31 + hours) % 1000000007
        total += hours
        if hours == 0:
            none += 1
    print(f"3000 contests: checksum {check}, {total} hours in all, {none} needing none")


if __name__ == "__main__":
    main()
