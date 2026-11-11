# LeetCode #1117: Building H2O -- mirrors the ★ arm: a hydrogen hands a
# one-slot queue to the oxygens and waits on it; an oxygen takes the
# bonding lock, receives two hydrogens, releases itself, sends each a
# queue to say it is out on, and waits for both before it lets go.
import queue
import threading


class H2O:
    def __init__(self):
        self.bonding = threading.Lock()
        self.hydrogens = queue.Queue(2)

    def hydrogen(self, release_hydrogen):
        go = queue.Queue(1)
        self.hydrogens.put(go)
        out = go.get()
        release_hydrogen()
        out.put(())

    def oxygen(self, release_oxygen):
        with self.bonding:
            gos = [self.hydrogens.get() for _ in range(2)]
            release_oxygen()
            out = queue.Queue(2)
            for go in gos:
                go.put(out)
            for _ in range(2):
                out.get()


state = [1117]


def next_random():
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def run(water):
    log = []
    lock = threading.Lock()

    def say(s):
        def p():
            with lock:
                log.append(s)
        return p

    h2o = H2O()
    ts = []
    for c in water:
        if c == "H":
            ts.append(threading.Thread(target=h2o.hydrogen, args=(say("H"),)))
        else:
            ts.append(threading.Thread(target=h2o.oxygen, args=(say("O"),)))
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return "".join(log)


def molecules(out):
    return sum(1 for i in range(len(out) // 3) if out[3 * i:3 * i + 3].count("H") == 2)


def water_of(n):
    atoms = list("OHH" * n)
    for j in range(len(atoms)):
        k = j + next_random() % (len(atoms) - j)
        atoms[j], atoms[k] = atoms[k], atoms[j]
    return "".join(atoms)


def show(water):
    out = run(water)
    return f"{water}: {len(out)} atoms, {molecules(out)} of {len(water) // 3} molecules whole"


print(show("HOH"))
print(show("OOHHHH"))
print(show("HHHHOO"))
print(show("OHHOHHOHH"))
right = 0
atoms = 0
for _ in range(2000):
    n = next_random() % 12 + 1
    water = water_of(n)
    out = run(water)
    atoms += len(out)
    if molecules(out) == n:
        right += 1
print(f"2000 random waters of up to 12 molecules: {atoms} atoms, {right} with every molecule whole")
print(show("O" * 20 + "H" * 40))
