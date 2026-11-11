# LeetCode #1125: Smallest Sufficient Team -- the bench in Python: the ★
# arm over 8 problems of 16 skills and 60 people, built once, each of 8
# rounds giving one person in every problem a skill or taking one away,
# and solving the problem again.


def smallest_sufficient_team(req_skills, people):
    bit = {s: i for i, s in enumerate(req_skills)}
    full = (1 << len(req_skills)) - 1
    team = [None] * (full + 1)
    team[0] = []
    for p, skills in enumerate(people):
        mask = 0
        for s in skills:
            mask |= 1 << bit[s]
        if mask == 0:
            continue
        for m in range(full + 1):
            if team[m] is None:
                continue
            grown = m | mask
            if grown == m:
                continue
            if team[grown] is None or len(team[m]) + 1 < len(team[grown]):
                team[grown] = team[m] + [p]
    return team[full]


seed = 1125


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    req = [f"s{i}" for i in range(16)]
    problems = []
    for _ in range(8):
        people = []
        for _ in range(60):
            people.append([s for s in req if next_random() % 100 < 20])
        problems.append(people)
    total = 0
    check = 0
    for rnd in range(8):
        for people in problems:
            who = next_random() % 60
            skill = f"s{next_random() % 16}"
            if skill in people[who]:
                people[who].remove(skill)
            else:
                people[who].append(skill)
            for s in req:
                if not any(s in p for p in people):
                    people[(who + 1) % 60].append(s)
            team = smallest_sufficient_team(req, people)
            total += len(team)
            for p in team:
                check = (check * 61 + p + 1) % 1000000007
            check = (check * 17 + rnd) % 1000000007
    print(f"8 rounds over 8 problems of 16 skills and 60 people: team sizes total {total}, checksum {check}")


main()
