// Benchmark for #519: Rust mirror of the ★ arm (a shuffle kept in a
// map); see random_flip_matrix.kara. `HashMap` with its default hasher,
// as the ★ arm's `Map`, a fresh one for every grid.
use std::collections::HashMap;

struct Draw {
    seed: i64,
}

impl Draw {
    fn step(&mut self) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        self.seed / 65536
    }

    // Uniform in [0, n) for n up to 2^30: 30 random bits, drawn again
    // when they land in the last, incomplete run of n.
    fn below(&mut self, n: i64) -> i64 {
        let limit = 1073741824 / n * n;
        loop {
            let high = self.step();
            let low = self.step();
            let r = high * 32768 + low;
            if r < limit {
                return r % n;
            }
        }
    }
}

struct Solution {
    m: i64,
    n: i64,
    free: i64,
    moved: HashMap<i64, i64>,
    draw: Draw,
}

impl Solution {
    fn new(m: i64, n: i64, seed: i64) -> Solution {
        Solution { m, n, free: m * n, moved: HashMap::new(), draw: Draw { seed } }
    }

    // What slot `i` of the shuffled cells holds.
    fn at(&self, i: i64) -> i64 {
        *self.moved.get(&i).unwrap_or(&i)
    }

    fn flip(&mut self) -> Vec<i64> {
        let r = self.draw.below(self.free);
        self.free -= 1;
        let cell = self.at(r);
        let last = self.at(self.free);
        self.moved.insert(r, last);
        vec![cell / self.n, cell % self.n]
    }

    fn reset(&mut self) {
        self.moved.clear();
        self.free = self.m * self.n;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10,000 grids of up to 10,000 by 10,000, 1,000 calls on each: a
    // reset one time in a hundred and whenever the grid is full, else a
    // flip.
    let mut seed: i64 = 519;
    let mut checksum: i64 = 0;
    let grids = 10000;
    for g in 0..grids {
        let high = next_random(&mut seed);
        let m = 1 + (high * 32768 + next_random(&mut seed)) % 10000;
        let high = next_random(&mut seed);
        let n = 1 + (high * 32768 + next_random(&mut seed)) % 10000;
        let mut solution = Solution::new(m, n, g);
        let mut free = m * n;
        for _ in 0..1000 {
            if free == 0 || next_random(&mut seed) % 100 == 0 {
                solution.reset();
                free = m * n;
            } else {
                let p = solution.flip();
                free -= 1;
                checksum = (checksum * 31 + p[0] * 10000 + p[1]) % 1000000007;
            }
        }
    }
    println!("{} grids, 1000 calls each: checksum {}", grids, checksum);
}
