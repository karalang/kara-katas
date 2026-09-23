// Benchmark mirror of LeetCode #323 — same disjoint-set forest as
// bench/count_components.kara.

const NODES: i64 = 1000000;
const PASSES: i64 = 16;
const STRIDE: i64 = 9973;
const MODULUS: i64 = 1073741789;

struct DisjointSet {
    parent: Vec<i64>,
    size: Vec<i64>,
    sets: i64,
}

impl DisjointSet {
    fn new(n: i64) -> DisjointSet {
        DisjointSet { parent: vec![0; n as usize], size: vec![1; n as usize], sets: n }
    }

    fn reset(&mut self) {
        for i in 0..self.parent.len() {
            self.parent[i] = i as i64;
            self.size[i] = 1;
        }
        self.sets = self.parent.len() as i64;
    }

    fn find(&mut self, x: i64) -> i64 {
        let mut root = x;
        while self.parent[root as usize] != root {
            root = self.parent[root as usize];
        }
        let mut cur = x;
        while self.parent[cur as usize] != root {
            let next = self.parent[cur as usize];
            self.parent[cur as usize] = root;
            cur = next;
        }
        root
    }

    fn merge(&mut self, a: i64, b: i64) {
        let mut ra = self.find(a);
        let mut rb = self.find(b);
        if ra == rb {
            return;
        }
        if self.size[ra as usize] < self.size[rb as usize] {
            std::mem::swap(&mut ra, &mut rb);
        }
        self.parent[rb as usize] = ra;
        self.size[ra as usize] += self.size[rb as usize];
        self.sets -= 1;
    }
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64, bound: i64) -> i64 {
    let hi = next(seed);
    let lo = next(seed);
    (hi * 32768 + lo) % bound
}

fn main() {
    let mut seed: i64 = 323;
    let mut sink: i64 = 0;
    let mut ds = DisjointSet::new(NODES);
    for p in 0..PASSES {
        ds.reset();
        let m = (1 + p % 4) * NODES / 4;
        for _ in 0..m {
            let a = draw(&mut seed, NODES);
            let b = draw(&mut seed, NODES);
            ds.merge(a, b);
        }
        let mut probe: i64 = 0;
        let mut i = 0;
        while i < NODES {
            probe = (probe * 31 + ds.find(i)) % MODULUS;
            i += STRIDE;
        }
        sink = (sink * 131 + ds.sets + probe) % MODULUS;
    }
    println!("sink {} components {}", sink, ds.sets);
}
