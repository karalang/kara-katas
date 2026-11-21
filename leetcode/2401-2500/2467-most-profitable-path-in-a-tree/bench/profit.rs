// LeetCode #2467: Most Profitable Path in a Tree -- the bench, the ★ arm in
// Rust: breadth-first parents and depths from node 0 over `Vec`
// adjacency lists, Bob's seconds up his parent chain, and each node's
// income its parent's plus its gate.

fn most_profitable_path(edges: &[Vec<i64>], bob: i64, amount: &[i64]) -> i64 {
    let n = amount.len();
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in edges {
        adjacent[e[0] as usize].push(e[1] as usize);
        adjacent[e[1] as usize].push(e[0] as usize);
    }
    let mut parent = vec![-1i64; n];
    let mut depth = vec![0i64; n];
    let mut order: Vec<usize> = vec![0];
    parent[0] = 0;
    let mut next = 0;
    while next < order.len() {
        let node = order[next];
        next += 1;
        for &child in &adjacent[node] {
            if parent[child] < 0 {
                parent[child] = node as i64;
                depth[child] = depth[node] + 1;
                order.push(child);
            }
        }
    }
    let mut bob_time = vec![n as i64; n];
    let mut node = bob as usize;
    let mut t = 0;
    while node != 0 {
        bob_time[node] = t;
        node = parent[node] as usize;
        t += 1;
    }
    bob_time[0] = t;
    let mut income = vec![0i64; n];
    let mut best = i64::MIN;
    for &node in &order {
        let gate = if depth[node] < bob_time[node] {
            amount[node]
        } else if depth[node] == bob_time[node] {
            amount[node] / 2
        } else {
            0
        };
        income[node] = if node == 0 { gate } else { income[parent[node] as usize] + gate };
        if node != 0 && adjacent[node].len() == 1 {
            best = best.max(income[node]);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10 random trees of 10^4 nodes built once, each node joined to an
    // earlier one, with even amounts from -10^4 to 10^4; then 140
    // passes, each moving every tree's Bob and setting one amount from the
    // checksum so far, then answering it and folding the answer plus the
    // pass into the checksum
    let mut seed = 2467;
    let n: i64 = 10000;
    let mut trees: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut amounts: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut edges: Vec<Vec<i64>> = Vec::new();
        for node in 1..n {
            let r = next_random(&mut seed);
            edges.push(vec![node, (r * 32768 + next_random(&mut seed)) % node]);
        }
        trees.push(edges);
        amounts.push((0..n).map(|_| 2 * (next_random(&mut seed) % 10001) - 10000).collect());
    }
    let mut check = 0i64;
    for p in 0..140i64 {
        for a in 0..trees.len() {
            let bob = 1 + check % (n - 1);
            amounts[a][((check + a as i64) % n) as usize] = 2 * (check % 10001) - 10000;
            let got = most_profitable_path(&trees[a], bob, &amounts[a]);
            check = ((check * 31 + got + p) % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("140 passes over 10 trees of 10^4: checksum {}", check);
}
