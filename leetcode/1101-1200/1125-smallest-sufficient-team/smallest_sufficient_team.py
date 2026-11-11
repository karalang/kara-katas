# LeetCode #1125: Smallest Sufficient Team -- the Python mirror of the ★
# arm: each skill a bit, each person a mask of their skills, and `team[m]`
# the smallest team found so far whose skills make the mask `m`, grown one
# person at a time over every mask already reached.


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


# ---- test harness ----

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def covers(req_skills, people, team):
    have = set()
    for p in team:
        have.update(people[p])
    return len(set(team)) == len(team) and all(0 <= p < len(people) for p in team) and all(s in have for s in req_skills)


# `m` skills named `s0`.. and `n` people, each with every skill at chance
# `percent` in 100, then any skill nobody has given to a random person.
def random_problem(m, n, percent):
    req = [f"s{i}" for i in range(m)]
    people = []
    for _ in range(n):
        people.append([s for s in req if next_random() % 100 < percent])
    for s in req:
        if not any(s in p for p in people):
            people[next_random() % n].append(s)
    return req, people


def report(req, people):
    team = smallest_sufficient_team(req, people)
    return f"a team of {len(team)}, {'covering every skill' if covers(req, people, team) else 'MISSING A SKILL'}"


def main():
    global seed
    cases = [
        (["java", "nodejs", "reactjs"], [["java"], ["nodejs"], ["nodejs", "reactjs"]]),
        (["algorithms", "math", "java", "reactjs", "csharp", "aws"],
         [["algorithms", "math", "java"], ["algorithms", "math", "reactjs"], ["java", "csharp", "aws"],
          ["reactjs", "csharp"], ["csharp", "math"], ["aws", "java"]]),
        (["a"], [["a"]]),
        (["a", "b", "c"], [[], ["a"], [], ["b"], ["c"], []]),
        (["a", "b", "c", "d"], [["a", "b"], ["c", "d"], ["a", "b", "c", "d"]]),
        (["a", "b", "c", "d"], [["a", "b", "c"], ["b", "c", "d"], ["a"], ["d"]]),
        (["a", "b", "c", "d", "e", "f"], [["a", "b", "c", "d"], ["a", "e"], ["b", "f"], ["c", "d", "e", "f"]]),
        (["x", "y"], [["x"], ["x"], ["y"], ["y"], ["x", "y"]]),
    ]
    for k, (req, people) in enumerate(cases):
        print(f"case {k + 1}, skills {len(req)}, people {len(people)}: {report(req, people)}")
    seed = 1125
    total = 0
    check = 0
    for t in range(500):
        m = next_random() % 10 + 1
        n = next_random() % 20 + 1
        req, people = random_problem(m, n, 10 + t % 4 * 10)
        team = smallest_sufficient_team(req, people)
        ok = 1 if covers(req, people, team) else 0
        total += len(team)
        check = (check * 31 + len(team) * 2 + ok) % 1000000007
    print(f"500 random problems: team sizes total {total}, checksum {check}")
    for percent in [5, 20]:
        req, people = random_problem(16, 60, percent)
        print(f"16 skills, 60 people at {percent}%: {report(req, people)}")


main()
