"""Writes data/ for mini_raft: six cluster scenarios for the Raft
simulator and one with mistakes in it.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

SCENARIOS = {
    "1_basic.sim": """# Three nodes elect a leader and replicate a few writes.
nodes 3
seed 11
until 1500
400 client n1 set x 1
420 client n2 set y 2
430 client n3 incr x 5
600 status
900 client n1 del y
910 client n2 incr hits 1
920 client n3 incr hits 1
""",
    "2_leader_crash.sim": """# The leader crashes; the rest elect a new one, and the old
# leader comes back as a follower and catches up.
nodes 5
seed 23
until 3000
400 client n1 set config v1
410 client n2 set config v1
420 client n3 set config v1
430 client n4 set config v1
440 client n5 set config v1
700 crash leader
900 client n1 set config v2
905 client n2 set config v2
910 client n3 set config v2
915 client n4 set config v2
920 client n5 set config v2
1200 status
1500 restart all
2000 status
""",
    "3_partition.sim": """# The leader is cut off with one follower. It keeps taking writes it
# cannot commit; the majority side elects a leader of its own and goes
# on. After the heal the old leader's uncommitted entries are replaced.
nodes 5
seed 5
until 4000
500 client leader set owner alice
800 partition leader+1
900 client minority set owner bob
905 client minority incr seats 2
1500 client majority set owner carol
1510 client majority incr seats 7
1700 status
2500 heal
3200 status
3300 client leader incr seats 1
""",
    "4_flaky.sim": """# A lossy network: 30% of messages are dropped. Elections take
# longer and some appends need retries, but nothing is lost.
nodes 5
seed 99
until 6000
200 drop 300
600 client leader set k1 a
1200 client leader set k2 b
1800 client leader set k3 c
2400 client leader incr n 1
3000 client leader incr n 1
3600 client leader incr n 1
4000 drop 0
4500 status
""",
    "5_churn.sim": """# Followers crash and restart while writes go on; at one point two
# are down at once, which leaves a majority of three.
nodes 5
seed 41
until 5000
400 client leader set a 1
600 crash follower
700 client leader incr a 1
900 crash follower
1000 client leader incr a 1
1300 restart all
1400 client leader incr a 1
1600 crash leader
2200 client leader incr a 10
2400 status
2600 restart all
3000 crash follower
3100 crash follower
3200 crash follower
3300 client leader incr a 100
3600 status
3700 restart all
4400 status
""",
    "6_isolated.sim": """# A follower is partitioned alone. Its elections fail, its term
# climbs, and on the heal its higher term forces a new election.
nodes 3
seed 8
until 4000
400 client leader set mode on
600 partition follower
1000 client leader set mode off
2600 status
2700 heal
3500 status
3600 client leader set mode auto
""",
    "7_bad.sim": """# Mistakes the loader reports.
nodes 3
seed 1
until 500
frobnicate
100 client n9 set x 1
200 explode n1
300 partition
nodes 99
""",
}
for name, text in SCENARIOS.items():
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
