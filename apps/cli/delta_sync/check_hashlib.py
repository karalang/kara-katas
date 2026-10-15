# Cross-check the mirror's hand-written pieces: its MD5 against hashlib on
# every file it writes and on edge-length inputs, and its rolling checksum
# against a direct sum at every window of the source files. Run it in an
# empty directory.
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import delta_sync as d

d.build_trees()
n = 0
for data in [b"", b"a", b"abc", bytes(55), bytes(56), bytes(63), bytes(64), bytes(119), bytes(1000)]:
    assert d.md5(data) == hashlib.md5(data).hexdigest(), data
    n += 1
for top in ("src", "dst"):
    for name in os.listdir(top):
        data = d.read(f"{top}/{name}")
        assert d.md5(data) == hashlib.md5(data).hexdigest(), name
        n += 1
windows = 0
for name in os.listdir("src"):
    data = d.read(f"src/{name}")
    if len(data) < d.BLOCK:
        continue
    a, b = d.weak(data, 0, d.BLOCK)
    for i in range(len(data) - d.BLOCK):
        assert (a, b) == d.weak(data, i, d.BLOCK), (name, i)
        x, y = data[i], data[i + d.BLOCK]
        a = (a - x + y) % d.MOD
        b = (b - d.BLOCK * x + a) % d.MOD
        windows += 1
print(f"md5 matches hashlib on {n} inputs; rolling checksum matches at {windows} windows")
