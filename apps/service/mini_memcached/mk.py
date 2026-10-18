# The input of mini_memcached: client sessions in the memcached text
# protocol. Run as a script, it writes data/sessions.txt; the mirror and
# gen_kara.py import FILES.
import os

S = []


def session(name, advance, lines):
    S.append("=== %s" % name)
    if advance:
        S.append("@advance %d" % advance)
    S.extend(lines)


session("basics", 0, [
    "version",
    "set user:1 0 0 5", "alice",
    "get user:1",
    "add user:1 0 0 3", "bob",
    "add user:2 7 0 3", "bob",
    "get user:1 user:2 user:3",
    "replace user:3 0 0 1", "x",
    "replace user:2 9 0 5", "carol",
    "gets user:2",
    "append user:1 0 0 6", "-smith",
    "prepend user:1 0 0 3", "dr.",
    "get user:1",
    "delete user:2",
    "delete user:2",
    "get user:2",
])

session("cas", 0, [
    "gets user:1",
    "cas user:1 0 0 3 4", "eve",
    "cas user:1 0 0 3 5", "eve",
    "gets user:1",
    "cas user:9 0 0 3 1", "eve",
    "set n 0 0 2 noreply", "41",
    "incr n 1",
    "gets n",
    "cas n 0 0 2 9 noreply", "99",
    "get n",
])

session("counters", 0, [
    "set hits 0 0 1", "9",
    "incr hits 1",
    "incr hits 90",
    "decr hits 7",
    "decr hits 1000",
    "set big 0 0 20", "18446744073709551615",
    "incr big 2",
    "incr hits abc",
    "incr user:1 1",
    "incr nope 1",
    "decr nope 1",
    "get hits big",
])

session("expiry", 0, [
    "set short 0 10 2", "ok",
    "set long 0 3600 2", "ok",
    "set forever 0 0 2", "ok",
    "set gone 0 -1 2", "ok",
    "set abs 0 1760000030 2", "ok",
    "set past 0 1759999000 2", "ok",
    "get short long forever gone abs past",
    "touch long 5",
    "touch missing 5",
])

session("later", 20, [
    "get short long forever abs",
    "gat 100 forever",
    "gats 0 forever",
])

session("much later", 40, [
    "get long abs forever",
    "flush_all 10",
    "get forever",
])

session("after the flush", 15, [
    "get forever user:1 n",
    "set fresh 0 0 3", "new",
    "get fresh",
])

session("eviction", 0, [
    "flush_all",
] + sum([["set k%d 0 0 200" % i, chr(ord("a") + i) * 200] for i in range(8)], []) + [
    "get k0",
    "set k8 0 0 200", "i" * 200,
    "set k9 0 0 200", "j" * 200,
    "get k0 k1 k2 k3",
    "set huge 0 0 3000", "x" * 3000,
    "get huge",
])

session("errors", 0, [
    "set k 0 0 3", "abcd",
    "get",
    "frobnicate now",
    "set bad 0 zero 2", "hi",
    "set toolong 0 0", 
    "get " + "k" * 251,
    "delete k0 0",
    "verbosity 1",
    "incr",
])

session("stats", 0, [
    "stats",
    "quit",
    "get fresh",
])

FILES = {"sessions.txt": "\n".join(S) + "\n"}


def write_all():
    for name, text in FILES.items():
        path = os.path.join("data", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            f.write(text)


if __name__ == "__main__":
    write_all()
