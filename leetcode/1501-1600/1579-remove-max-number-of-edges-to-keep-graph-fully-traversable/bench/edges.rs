// LeetCode #1579 bench: the same two union-find structs, in Rust.

struct Dsu {
    parent: Vec<i64>,
    size: Vec<i64>,
    parts: i64,
}

impl Dsu {
    fn new(n: i64) -> Dsu {
        Dsu { parent: (0..n + 1).collect(), size: vec![1; (n + 1) as usize], parts: n }
    }

    fn find(&mut self, x: i64) -> i64 {
        let mut x = x as usize;
        while self.parent[x] != x as i64 {
            self.parent[x] = self.parent[self.parent[x] as usize];
            x = self.parent[x] as usize;
        }
        x as i64
    }

    fn join(&mut self, a: i64, b: i64) -> bool {
        let ra = self.find(a) as usize;
        let rb = self.find(b) as usize;
        if ra == rb {
            return false;
        }
        let (big, small) = if self.size[ra] < self.size[rb] { (rb, ra) } else { (ra, rb) };
        self.parent[small] = big as i64;
        self.size[big] += self.size[small];
        self.parts -= 1;
        true
    }
}

fn max_num_edges_to_remove(n: i64, edges: &[Vec<i64>]) -> i64 {
    let mut alice = Dsu::new(n);
    let mut bob = Dsu::new(n);
    let mut kept = 0i64;
    for e in edges.iter() {
        if e[0] == 3 {
            let a = alice.join(e[1], e[2]);
            let b = bob.join(e[1], e[2]);
            if a || b {
                kept += 1;
            }
        }
    }
    for e in edges.iter() {
        if e[0] == 1 && alice.join(e[1], e[2]) {
            kept += 1;
        }
        if e[0] == 2 && bob.join(e[1], e[2]) {
            kept += 1;
        }
    }
    if alice.parts != 1 || bob.parts != 1 {
        return -1;
    }
    edges.len() as i64 - kept
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1579i64;
    let mut graphs: Vec<(i64, Vec<Vec<i64>>)> = Vec::new();
    for _ in 0..40 {
        let n = 13000i64;
        let mut edges: Vec<Vec<i64>> = Vec::new();
        for u in 1..n {
            for _ in 0..next_random(&mut seed) % 8 + 4 {
                let kind = (next_random(&mut seed) % 4).min(2) + 1;
                let v = (u + 1 + next_random(&mut seed) % 12).min(n);
                edges.push(vec![kind, u, v]);
            }
        }
        for i in (1..edges.len()).rev() {
            let j = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % (i as i64 + 1)) as usize;
            edges.swap(i, j);
        }
        graphs.push((n, edges));
    }
    let (mut check, mut total, mut stuck) = (0i64, 0i64, 0i64);
    for (n, edges) in graphs.iter() {
        let removed = max_num_edges_to_remove(*n, edges);
        if removed < 0 {
            stuck += 1;
        } else {
            total += removed;
        }
        check = mix(check, removed + 1);
    }
    println!("40 graphs of 13000 nodes: {} not traversable, edges removed {}, checksum {}", stuck, total, check);
}
