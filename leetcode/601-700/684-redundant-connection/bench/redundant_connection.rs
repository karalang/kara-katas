// LeetCode #684: Redundant Connection -- union-find. Bench.
//
// 100 random trees of 20,000 vertices, each with one more edge, are
// built once; then 30 rounds answer every graph.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut v = x;
    while parent[v as usize] != v {
        parent[v as usize] = parent[parent[v as usize] as usize];
        v = parent[v as usize];
    }
    v
}

fn find_redundant_connection(edges: &[(i64, i64)]) -> (i64, i64) {
    let n = edges.len();
    let mut parent: Vec<i64> = (0..=n as i64).collect();
    let mut size: Vec<i64> = vec![1; n + 1];
    for &(a, b) in edges {
        let ra = find(&mut parent, a);
        let rb = find(&mut parent, b);
        if ra == rb {
            return (a, b);
        }
        let (ra, rb) = (ra as usize, rb as usize);
        if size[ra] < size[rb] {
            parent[ra] = rb as i64;
            size[rb] += size[ra];
        } else {
            parent[rb] = ra as i64;
            size[ra] += size[rb];
        }
    }
    (0, 0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 100;
    let n: i64 = 20000;
    let rounds: i64 = 30;
    let mut seed: i64 = 684;
    let mut graphs: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..count {
        let mut name: Vec<i64> = (1..=n).collect();
        let mut i = n - 1;
        while i > 0 {
            let j = next_random(&mut seed) % (i + 1);
            name.swap(i as usize, j as usize);
            i -= 1;
        }
        let mut up: Vec<i64> = vec![0; n as usize];
        let mut edges: Vec<(i64, i64)> = Vec::new();
        for v in 1..n {
            up[v as usize] = next_random(&mut seed) % v;
            edges.push((name[up[v as usize] as usize], name[v as usize]));
        }
        loop {
            let x = next_random(&mut seed) % n;
            let y = next_random(&mut seed) % n;
            let (lo, hi) = if x < y { (x, y) } else { (y, x) };
            if lo != hi && up[hi as usize] != lo {
                edges.push((name[lo as usize], name[hi as usize]));
                break;
            }
        }
        let mut k = n - 1;
        while k > 0 {
            let j = next_random(&mut seed) % (k + 1);
            edges.swap(k as usize, j as usize);
            k -= 1;
        }
        for e in 0..n as usize {
            if next_random(&mut seed) % 2 == 0 {
                let (a, b) = edges[e];
                edges[e] = (b, a);
            }
        }
        graphs.push(edges);
    }
    let mut sum: i64 = 0;
    for r in 0..rounds {
        for c in 0..count as usize {
            let (a, b) = find_redundant_connection(&graphs[c]);
            sum = (sum * 31 + a * 20011 + b + r) % 1000000007;
        }
    }
    println!("{} graphs answered, checksum {}", count * rounds, sum);
}
