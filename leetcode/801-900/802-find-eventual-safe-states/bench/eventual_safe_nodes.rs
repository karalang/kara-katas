// LeetCode 802 -- Find Eventual Safe States: the bench, mirroring
// eventual_safe_nodes.kara with the same three-colour search.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn is_safe(graph: &[Vec<i64>], node: i64, colour: &mut Vec<i64>) -> bool {
    if colour[node as usize] != 0 {
        return colour[node as usize] == 2;
    }
    colour[node as usize] = 1;
    for &next in graph[node as usize].iter() {
        if !is_safe(graph, next, colour) {
            return false;
        }
    }
    colour[node as usize] = 2;
    true
}

fn eventual_safe_nodes(graph: &[Vec<i64>]) -> Vec<i64> {
    let n = graph.len() as i64;
    // 0 not seen yet, 1 grey (on the search or unsafe), 2 black (safe).
    let mut colour: Vec<i64> = Vec::new();
    for _ in 0..n {
        colour.push(0);
    }
    let mut safe: Vec<i64> = Vec::new();
    for node in 0..n {
        if is_safe(graph, node, &mut colour) {
            safe.push(node);
        }
    }
    safe
}

fn main() {
    let n: i64 = 10000;
    let mut seed: i64 = 802;
    let mut graphs: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..16 {
        let mut graph: Vec<Vec<i64>> = Vec::new();
        for a in 0..n {
            let mut picked: Vec<i64> = Vec::new();
            let edges = next_random(&mut seed) % 5;
            for _ in 0..edges {
                let b = if next_random(&mut seed) % 1000 == 0 {
                    (a - 1 - next_random(&mut seed) % 50).max(0)
                } else {
                    a + 1 + next_random(&mut seed) % 50
                };
                if b < n {
                    picked.push(b);
                }
            }
            // In increasing order with no edge twice, as LeetCode gives.
            picked.sort();
            let mut out: Vec<i64> = Vec::new();
            for &b in picked.iter() {
                if out.is_empty() || out[out.len() - 1] != b {
                    out.push(b);
                }
            }
            graph.push(out);
        }
        graphs.push(graph);
    }
    let rounds: i64 = 4000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let safe = eventual_safe_nodes(&graphs[(r % 16) as usize]);
        let count = safe.len() as i64;
        total += count;
        check = (check * 131 + count + safe[safe.len() / 2]) % 1000000007;
    }
    println!("{} rounds of {} nodes: {} safe nodes in all, checksum {}", rounds, n, total, check);
}
