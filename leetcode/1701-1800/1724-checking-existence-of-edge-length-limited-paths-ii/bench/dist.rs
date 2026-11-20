// LeetCode #1724: Checking Existence of Edge Length Limited Paths II --
// the bench (dist.kara): a union-find by rank, never compressed, each
// node keeping the weight of the edge that hung it under its parent; a
// query climbs from each node while the links stay below the limit.

struct DistanceLimitedPathsExist {
    parent: Vec<usize>,
    joined: Vec<i32>,
}

fn root(parent: &[usize], x: usize) -> usize {
    let mut x = x;
    while parent[x] != x {
        x = parent[x];
    }
    x
}

impl DistanceLimitedPathsExist {
    fn new(n: i32, edge_list: &[Vec<i32>]) -> Self {
        let n = n as usize;
        let mut edges = edge_list.to_vec();
        edges.sort_by_key(|e| e[2]);
        let mut parent: Vec<usize> = (0..n).collect();
        let mut joined = vec![i32::MAX; n];
        let mut rank = vec![0u32; n];
        for e in edges.iter() {
            let mut a = root(&parent, e[0] as usize);
            let mut b = root(&parent, e[1] as usize);
            if a == b {
                continue;
            }
            if rank[a] < rank[b] {
                std::mem::swap(&mut a, &mut b);
            }
            parent[b] = a;
            joined[b] = e[2];
            if rank[a] == rank[b] {
                rank[a] += 1;
            }
        }
        DistanceLimitedPathsExist { parent, joined }
    }

    fn root_below(&self, x: usize, limit: i32) -> usize {
        let mut x = x;
        while self.joined[x] < limit {
            x = self.parent[x];
        }
        x
    }

    fn query(&self, p: i32, q: i32, limit: i32) -> bool {
        self.root_below(p as usize, limit) == self.root_below(q as usize, limit)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let count = 20;
    let rounds: i64 = 50;
    let n: i64 = 10000;
    let m = 10000;
    let asked = 10000;
    let top: i64 = 1000000000;
    let mut seed: i64 = 1724;
    let mut problems: Vec<(Vec<Vec<i32>>, Vec<(i32, i32, i32)>)> = Vec::new();
    for _ in 0..count {
        let mut edge_list: Vec<Vec<i32>> = Vec::new();
        for _ in 0..m {
            let u = wide(&mut seed) % n;
            let mut v = wide(&mut seed) % (n - 1);
            if v >= u {
                v += 1;
            }
            edge_list.push(vec![u as i32, v as i32, (wide(&mut seed) % top + 1) as i32]);
        }
        let mut queries: Vec<(i32, i32, i32)> = Vec::new();
        for _ in 0..asked {
            let p = wide(&mut seed) % n;
            let mut q = wide(&mut seed) % (n - 1);
            if q >= p {
                q += 1;
            }
            queries.push((p as i32, q as i32, (wide(&mut seed) % top + 1) as i32));
        }
        problems.push((edge_list, queries));
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (edge_list, queries) in problems.iter() {
            let graph = DistanceLimitedPathsExist::new(n as i32, edge_list);
            for &(p, q, limit) in queries.iter() {
                let answer = graph.query(p, q, limit);
                if answer {
                    yes += 1;
                }
                check = (check * 31 + if answer { 2 } else { 1 } + r) % 1000000007;
            }
        }
    }
    println!(
        "{} graphs of {} nodes and {} edges, {} queries each, {} rounds: {} paths, checksum {}",
        count, n, m, asked, rounds, yes, check
    );
}
