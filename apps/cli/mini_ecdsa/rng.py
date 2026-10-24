# The seeded stand-in for os.urandom that mk.py and oracle.py install, so
# key generation, padding and blinding are the same on every run. The port
# has the same generator: splitmix64, each read(n) taking ceil(n/8) words
# and their little-endian bytes.
M = (1 << 64) - 1


class Stream:
    def __init__(self, seed):
        self.state = seed & M

    def word(self):
        self.state = (self.state + 0x9E3779B97F4A7C15) & M
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M
        return z ^ (z >> 31)

    def read(self, n):
        out = b''
        while len(out) < n:
            out += self.word().to_bytes(8, 'little')
        return out[:n]
