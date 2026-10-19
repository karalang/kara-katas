// LeetCode 785 — Is Graph Bipartite?: the bench, in Rust.
// Mirrors is_bipartite.kara: two colours by breadth first search over the
// same 64 graphs.
use std::collections::VecDeque;

fn is_bipartite(graph: &Vec<Vec<i64>>) -> bool {
    let n = graph.len();
    let mut colour: Vec<i64> = vec![-1; n];
    let mut queue: VecDeque<usize> = VecDeque::new();
    for start in 0..n {
        if colour[start] != -1 {
            continue;
        }
        colour[start] = 0;
        queue.push_back(start);
        while let Some(u) = queue.pop_front() {
            for &v in graph[u].iter() {
                let v = v as usize;
                if colour[v] == -1 {
                    colour[v] = 1 - colour[u];
                    queue.push_back(v);
                } else if colour[v] == colour[u] {
                    return false;
                }
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 785;
    let mut graphs: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..64 {
        let side: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 2).collect();
        let mut graph: Vec<Vec<i64>> = vec![Vec::new(); 100];
        for a in 0..100 {
            for b in a + 1..100 {
                if side[a] != side[b] && next_random(&mut seed) % 10 == 0 {
                    graph[a].push(b as i64);
                    graph[b].push(a as i64);
                }
            }
        }
        if g % 2 == 1 {
            let a = (next_random(&mut seed) % 100) as usize;
            let mut b = (a + 1) % 100;
            while side[b] != side[a] {
                b = (b + 1) % 100;
            }
            graph[a].push(b as i64);
            graph[b].push(a as i64);
        }
        graphs.push(graph);
    }
    let rounds: i64 = 500000;
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let answer = is_bipartite(&graphs[(r % 64) as usize]);
        if answer {
            yes += 1;
        }
        check = (check * 31 + if answer { 2 } else { 1 } + r % 7) % 1000000007;
    }
    println!("{rounds} rounds of 100-node graphs: {yes} bipartite, checksum {check}");
}
