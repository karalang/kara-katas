// LeetCode #1168: Optimize Water Distribution in a Village -- the ★ arm's
// bench in Rust: Kruskal over the pipes and a pipe from a source to every
// house, union-find by size with path halving.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn min_cost_to_supply_water(n: i64, wells: &[i64], pipes: &[Vec<i64>]) -> i64 {
    let mut edges: Vec<(i64, i64, i64)> = Vec::new();
    for (i, &w) in wells.iter().enumerate() {
        edges.push((w, 0, i as i64 + 1));
    }
    for p in pipes {
        edges.push((p[2], p[0], p[1]));
    }
    edges.sort();
    let mut parent: Vec<i64> = (0..n + 1).collect();
    let mut size = vec![1i64; (n + 1) as usize];
    let mut cost = 0;
    let mut joined = 0;
    for (c, a, b) in edges {
        let mut ra = find(&mut parent, a);
        let mut rb = find(&mut parent, b);
        if ra == rb {
            continue;
        }
        if size[ra as usize] < size[rb as usize] {
            std::mem::swap(&mut ra, &mut rb);
        }
        parent[rb as usize] = ra;
        size[ra as usize] += size[rb as usize];
        cost += c;
        joined += 1;
        if joined == n {
            break;
        }
    }
    cost
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1168;
    let n = 10000;
    let mut wells: Vec<Vec<i64>> = Vec::new();
    let mut pipes: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..16 {
        wells.push((0..n).map(|_| next_random(&mut seed) % 100001).collect());
        let mut ps: Vec<Vec<i64>> = Vec::new();
        for _ in 0..10000 {
            let a = 1 + next_random(&mut seed) % n;
            let mut b = 1 + next_random(&mut seed) % (n - 1);
            if b >= a {
                b += 1;
            }
            ps.push(vec![a, b, next_random(&mut seed) % 100001]);
        }
        pipes.push(ps);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..40 {
        for v in 0..16 {
            let j = (next_random(&mut seed) % 10000) as usize;
            pipes[v][j][2] = next_random(&mut seed) % 100001;
            let c = min_cost_to_supply_water(n, &wells[v], &pipes[v]);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("40 rounds over 16 villages of 10^4 houses: total {}, checksum {}", total, check);
}
