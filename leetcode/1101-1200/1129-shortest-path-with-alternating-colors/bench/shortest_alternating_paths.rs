// LeetCode #1129: Shortest Path with Alternating Colors -- the bench in
// Rust, the ★ arm over `Vec<Vec<i64>>` edge lists: the adjacency built per
// call as one list per node and colour, a breadth-first search over (node,
// colour) with a `VecDeque`, the same 32 graphs and 1000 rounds.
use std::collections::VecDeque;

fn shortest_alternating_paths(n: i64, red_edges: &[Vec<i64>], blue_edges: &[Vec<i64>]) -> Vec<i64> {
    let n = n as usize;
    let mut adj: Vec<Vec<Vec<i64>>> = vec![vec![Vec::new(); n]; 2];
    for e in red_edges {
        adj[0][e[0] as usize].push(e[1]);
    }
    for e in blue_edges {
        adj[1][e[0] as usize].push(e[1]);
    }
    let mut dist = vec![vec![-1i64; n]; 2];
    dist[0][0] = 0;
    dist[1][0] = 0;
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    queue.push_back((0, 0));
    queue.push_back((0, 1));
    while let Some((node, colour)) = queue.pop_front() {
        let next = 1 - colour;
        for &m in &adj[next as usize][node as usize] {
            if dist[next as usize][m as usize] < 0 {
                dist[next as usize][m as usize] = dist[colour as usize][node as usize] + 1;
                queue.push_back((m, next));
            }
        }
    }
    (0..n)
        .map(|x| {
            let (a, b) = (dist[0][x], dist[1][x]);
            if a < 0 { b } else if b < 0 { a } else { a.min(b) }
        })
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn edges(seed: &mut i64, n: i64, m: i64) -> Vec<Vec<i64>> {
    let mut out: Vec<Vec<i64>> = Vec::new();
    for _ in 0..m {
        let a = next_random(seed) % n;
        let b = next_random(seed) % n;
        out.push(vec![a, b]);
    }
    out
}

fn main() {
    let mut seed = 1129;
    let mut reds: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut blues: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..32 {
        reds.push(edges(&mut seed, 100, 400));
        blues.push(edges(&mut seed, 100, 400));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..1000i64 {
        for j in 0..32usize {
            let at = ((round * 7919 + j as i64 * 104729) % 400) as usize;
            if round % 2 == 0 {
                reds[j][at][1] = (reds[j][at][1] + 1 + round % 7) % 100;
            } else {
                blues[j][at][1] = (blues[j][at][1] + 1 + round % 7) % 100;
            }
            let answer = shortest_alternating_paths(100, &reds[j], &blues[j]);
            for &d in &answer {
                total += d;
                check = (check * 31 + d + 2) % 1000000007;
            }
        }
    }
    println!("1000 rounds over 32 graphs of 100 nodes and 400 edges of each colour: lengths total {total}, checksum {check}");
}
