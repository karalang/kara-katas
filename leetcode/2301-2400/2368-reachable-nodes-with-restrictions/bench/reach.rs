// LeetCode #2368: Reachable Nodes With Restrictions -- the bench, the ★
// arm in Rust: adjacency lists, the restricted nodes marked, and a
// breadth-first search from node 0 that never enters a marked node.

fn reachable_nodes(n: usize, edges: &[(usize, usize)], restricted: &[usize]) -> i64 {
    let mut next: Vec<Vec<usize>> = vec![Vec::new(); n];
    for &(a, b) in edges {
        next[a].push(b);
        next[b].push(a);
    }
    let mut seen = vec![false; n];
    for &r in restricted {
        seen[r] = true;
    }
    seen[0] = true;
    let mut queue: Vec<usize> = vec![0];
    let mut head = 0;
    while head < queue.len() {
        let u = queue[head];
        head += 1;
        for &v in &next[u] {
            if !seen[v] {
                seen[v] = true;
                queue.push(v);
            }
        }
    }
    queue.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // tree a: 10^5 nodes, node i joined to one of the 4^a nodes before it,
    // and each node but 0 restricted with a chance of 1 in 2^(a + 4)
    let n = 100000usize;
    let mut seed = 2368i64;
    let mut trees: Vec<(Vec<(usize, usize)>, Vec<usize>)> = Vec::new();
    let mut width = 1i64;
    for a in 0..10 {
        let edges: Vec<(usize, usize)> =
            (1..n).map(|i| (i - 1 - (next_random(&mut seed) % width.min(i as i64)) as usize, i)).collect();
        let restricted: Vec<usize> = (1..n).filter(|_| next_random(&mut seed) % (16i64 << a) == 0).collect();
        trees.push((edges, restricted));
        width *= 4;
    }
    let mut check = 0i64;
    for p in 0..20i64 {
        for (edges, restricted) in &trees {
            check = (check * 31 + reachable_nodes(n, edges, restricted) + p) % 1000000007;
        }
    }
    println!("20 passes over 10 trees of 10^5 nodes: checksum {}", check);
}
