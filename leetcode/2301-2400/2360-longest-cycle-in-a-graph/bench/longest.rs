// LeetCode #2360: Longest Cycle in a Graph -- the bench, the ★ arm in
// Rust: each node stamped with the time it is first visited, and a walk
// that reaches a node stamped since it began has closed a cycle as long as
// the time between the two visits.

fn longest_cycle(edges: &[i64]) -> i64 {
    let n = edges.len();
    let mut stamp = vec![-1i64; n];
    let mut time = 0i64;
    let mut best = -1i64;
    for start in 0..n {
        let began = time;
        let mut node = start as i64;
        while node != -1 && stamp[node as usize] == -1 {
            stamp[node as usize] = time;
            time += 1;
            node = edges[node as usize];
        }
        if node != -1 && stamp[node as usize] >= began {
            best = best.max(time - stamp[node as usize]);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    // graph a: 10^5 nodes shuffled into one line, cut into pieces with a
    // chance of 1 in 2^(a + 4) at each link; each piece's last node points
    // back to its first with a chance of 1 in 2, and otherwise at a random
    // node
    let n = 100000usize;
    let mut seed = 2360i64;
    let mut graphs: Vec<Vec<i64>> = Vec::new();
    for a in 0..10i64 {
        let mut order: Vec<i64> = (0..n as i64).collect();
        for i in (1..n).rev() {
            let j = wide_random(&mut seed) % (i as i64 + 1);
            order.swap(i, j as usize);
        }
        let cut = 1i64 << (a + 4);
        let mut edges = vec![-1i64; n];
        let mut first = 0usize;
        for i in 0..n {
            if i == n - 1 || next_random(&mut seed) % cut == 0 {
                let target = if next_random(&mut seed) % 2 == 0 { order[first] } else { wide_random(&mut seed) % n as i64 };
                if target != order[i] {
                    edges[order[i] as usize] = target;
                }
                first = i + 1;
            } else {
                edges[order[i] as usize] = order[i + 1];
            }
        }
        graphs.push(edges);
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for edges in &graphs {
            check = (check * 31 + longest_cycle(edges) + 2 + p) % 1000000007;
        }
    }
    println!("50 passes over 10 graphs of 10^5 nodes: checksum {}", check);
}
