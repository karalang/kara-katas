# LeetCode #2383: Minimum Hours of Training to Win a Competition -- the
# bench, the ★ arm in Python: the energy trained to one above the
# opponents' sum, the experience walked through the opponents.


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


seed = 2383


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 1000 contests of 100 opponents, contest c's from 1 to 1 + c % 100;
    # pass p starts contest c with (p + c) % 50 more energy and
    # (3 p + c) % 50 more experience than its own start
    energies = []
    experiences = []
    starts = []
    for c in range(1000):
        top = 1 + c % 100
        ie = 1 + next_random() % 100
        ix = 1 + next_random() % 100
        starts.append((ie, ix))
        energies.append([1 + next_random() % top for _ in range(100)])
        experiences.append([1 + next_random() % top for _ in range(100)])
    check = 0
    for p in range(5000):
        for c in range(1000):
            ie, ix = starts[c]
            hours = min_number_of_hours(ie + (p + c) % 50, ix + (3 * p + c) % 50, energies[c], experiences[c])
            check = (check * 31 + hours + p) % 1000000007
    print(f"5000 passes over 1000 contests of 100 opponents: checksum {check}")


main()
