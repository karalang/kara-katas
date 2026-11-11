# LeetCode #1117: Building H2O -- the bench's Python mirror: a thread per
# atom; a hydrogen hands a one-slot queue to the oxygens and waits on it,
# and an oxygen takes the bonding lock, receives two hydrogens, releases
# itself, sends each a queue to say it is out on, and waits for both.
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


def run(water):
    lock = threading.Lock()
    log = []

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


def main():
    seed = 1117
    whole = 0
    check = 0
    for r in range(500):
        water = list("OHH" * 20)
        for j in range(60):
            seed = (seed * 1103515245 + 12345) % 2147483648
            k = j + seed // 65536 % (60 - j)
            water[j], water[k] = water[k], water[j]
        out = run(water)
        molecules = sum(1 for i in range(len(out) // 3) if out[3 * i:3 * i + 3].count("H") == 2)
        if molecules == 20:
            whole += 1
        check = (check * 31 + len(out) + r) % 1000000007
    print(f"500 runs of 20 molecules: {whole} with every molecule whole, checksum {check}")


main()
