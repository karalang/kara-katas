// LeetCode #2846: Minimum Edge Weight Equilibrium Queries in a Tree --
// the bench, mirrored from equilibrium.kara: weight counts from the
// root by a breadth-first walk, and each query's lowest common ancestor
// by binary lifting.
use std::collections::VecDeque;

fn min_operations_queries(n: usize, edges: &[Vec<i64>], queries: &[Vec<i64>]) -> Vec<i64> {
    let mut adj: Vec<Vec<(usize, usize)>> = vec![Vec::new(); n];
    for e in edges.iter() {
        let (u, v, w) = (e[0] as usize, e[1] as usize, e[2] as usize);
        adj[u].push((v, w));
        adj[v].push((u, w));
    }
    let levels = 15;
    let mut up: Vec<Vec<usize>> = vec![vec![0; n]; levels];
    let mut depth: Vec<i64> = vec![0; n];
    let mut count: Vec<Vec<i64>> = vec![vec![0; 27]; n];
    let mut seen: Vec<bool> = vec![false; n];
    let mut queue: VecDeque<usize> = VecDeque::new();
    seen[0] = true;
    queue.push_back(0);
    while let Some(v) = queue.pop_front() {
        for i in 0..adj[v].len() {
            let (u, w) = adj[v][i];
            if !seen[u] {
                seen[u] = true;
                up[0][u] = v;
                depth[u] = depth[v] + 1;
                count[u] = count[v].clone();
                count[u][w] += 1;
                queue.push_back(u);
            }
        }
    }
    for j in 1..levels {
        for v in 0..n {
            up[j][v] = up[j - 1][up[j - 1][v]];
        }
    }
    let lca = |a: usize, b: usize| {
        let (mut x, mut y) = if depth[a] >= depth[b] { (a, b) } else { (b, a) };
        for j in (0..levels).rev() {
            if depth[x] - (1 << j) >= depth[y] {
                x = up[j][x];
            }
        }
        if x == y {
            return x;
        }
        for j in (0..levels).rev() {
            if up[j][x] != up[j][y] {
                x = up[j][x];
                y = up[j][y];
            }
        }
        up[0][x]
    };
    queries
        .iter()
        .map(|q| {
            let (a, b) = (q[0] as usize, q[1] as usize);
            let c = lca(a, b);
            let on_path: Vec<i64> = (1..27).map(|w| count[a][w] + count[b][w] - 2 * count[c][w]).collect();
            on_path.iter().sum::<i64>() - on_path.iter().max().unwrap()
        })
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let n: i64 = 10000;
    let asked = 20000;
    let rounds = 5;
    let mut seed = 2846;
    let mut cases: Vec<(Vec<Vec<i64>>, Vec<Vec<i64>>)> = Vec::new();
    for _ in 0..count {
        let mut label: Vec<i64> = (0..n).collect();
        for i in (1..n).rev() {
            let j = next_random(&mut seed) % (i + 1);
            label.swap(i as usize, j as usize);
        }
        let edges: Vec<Vec<i64>> = (1..n)
            .map(|i| {
                let a = label[i as usize];
                let b = label[(next_random(&mut seed) % i) as usize];
                vec![a, b, next_random(&mut seed) % 26 + 1]
            })
            .collect();
        let queries: Vec<Vec<i64>> = (0..asked)
            .map(|_| {
                let a = next_random(&mut seed) % n;
                vec![a, next_random(&mut seed) % n]
            })
            .collect();
        cases.push((edges, queries));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (edges, queries) in cases.iter() {
            for ops in min_operations_queries(n as usize, edges, queries).iter() {
                total += ops;
                check = (check * 31 + ops + r) % 1000000007;
            }
        }
    }
    println!("{count} trees of {n}, {asked} queries, {rounds} rounds: {total} operations, checksum {check}");
}
