// LeetCode #2508: Add Edges to Make Degrees of All Nodes Even -- Rust
// mirror of the benchmark (even.kara): the same graphs, passes and
// checksum, the edges held in a `HashSet`.
use std::collections::HashSet;

fn is_possible(n: i64, edges: &[Vec<i64>]) -> bool {
    let mut degree = vec![0i64; (n + 1) as usize];
    let mut present: HashSet<i64> = HashSet::new();
    for edge in edges {
        let (a, b) = (edge[0], edge[1]);
        degree[a as usize] += 1;
        degree[b as usize] += 1;
        present.insert(a.min(b) * (n + 1) + a.max(b));
    }
    let free = |a: i64, b: i64| !present.contains(&(a.min(b) * (n + 1) + a.max(b)));
    let odd: Vec<i64> = (1..n + 1).filter(|&v| degree[v as usize] % 2 == 1).collect();
    match odd.len() {
        0 => true,
        2 => {
            let (a, b) = (odd[0], odd[1]);
            free(a, b) || (1..n + 1).any(|c| c != a && c != b && free(a, c) && free(b, c))
        }
        4 => {
            let (a, b, c, d) = (odd[0], odd[1], odd[2], odd[3]);
            (free(a, b) && free(c, d)) || (free(a, c) && free(b, d)) || (free(a, d) && free(b, c))
        }
        _ => false,
    }
}

fn ring_of(n: i64, step: i64) -> Vec<Vec<i64>> {
    (1..n + 1).map(|v| vec![v, (v + step - 1) % n + 1]).collect()
}

fn joined_ring(spare: i64) -> Vec<Vec<i64>> {
    let mut edges: Vec<Vec<i64>> = (3..33000).map(|v| vec![v, v + 1]).collect();
    edges.push(vec![33000, 3]);
    edges.push(vec![1, 2]);
    for v in 3..33001 {
        if v != spare {
            for h in [1, 2] {
                edges.push(vec![h, v]);
            }
        }
    }
    edges
}

fn main() {
    let passes = 90;
    let mut graphs: Vec<(i64, Vec<Vec<i64>>)> = vec![
        (100000, ring_of(100000, 1)),
        (100000, ring_of(100000, 2)),
        (33000, joined_ring(0)),
        (33000, joined_ring(17000)),
    ];
    let mut check: i64 = 0;
    for p in 0..passes {
        for g in graphs.iter_mut() {
            let n = g.0;
            let at = (check % g.1.len() as i64) as usize;
            let taken = g.1.swap_remove(at);
            let answer = if is_possible(n, &g.1) { 2 } else { 1 };
            check = (check * 31 + answer + p) % 1000000007;
            g.1.push(taken);
            let last = g.1.len() - 1;
            g.1.swap(at, last);
        }
    }
    println!("{} passes over 4 graphs: checksum {}", passes, check);
}
