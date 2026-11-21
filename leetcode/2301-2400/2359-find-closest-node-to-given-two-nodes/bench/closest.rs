// LeetCode #2359: Find Closest Node to Given Two Nodes -- the bench, the ★
// arm in Rust: each start's path walked for its distances, then every node
// both reach scanned for the least of the larger distance.

fn distances(edges: &[i64], start: i64) -> Vec<i64> {
    let mut dist = vec![-1i64; edges.len()];
    let mut node = start;
    let mut d = 0i64;
    while node != -1 && dist[node as usize] == -1 {
        dist[node as usize] = d;
        node = edges[node as usize];
        d += 1;
    }
    dist
}

fn closest_meeting_node(edges: &[i64], node1: i64, node2: i64) -> i64 {
    let d1 = distances(edges, node1);
    let d2 = distances(edges, node2);
    let mut best = -1i64;
    let mut best_dist = -1i64;
    for v in 0..edges.len() {
        if d1[v] >= 0 && d2[v] >= 0 {
            let far = d1[v].max(d2[v]);
            if best < 0 || far < best_dist {
                best = v as i64;
                best_dist = far;
            }
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
    // graph a: 10^5 nodes shuffled into one line, each link cut with a
    // chance of 1 in 2^(a + 4), the last node linked back to the first
    // when a is odd; 20 random pairs of starts in each
    let n = 100000i64;
    let mut seed = 2359i64;
    let mut graphs: Vec<Vec<i64>> = Vec::new();
    let mut starts: Vec<Vec<i64>> = Vec::new();
    for a in 0..10i64 {
        let mut order: Vec<i64> = (0..n).collect();
        for i in (1..n).rev() {
            let j = wide_random(&mut seed) % (i + 1);
            order.swap(i as usize, j as usize);
        }
        let cut = 1i64 << (a + 4);
        let mut edges = vec![-1i64; n as usize];
        for i in 0..(n - 1) as usize {
            if next_random(&mut seed) % cut != 0 {
                edges[order[i] as usize] = order[i + 1];
            }
        }
        if a % 2 == 1 {
            edges[order[(n - 1) as usize] as usize] = order[0];
        }
        graphs.push(edges);
        let pairs: Vec<i64> = (0..40).map(|_| wide_random(&mut seed) % n).collect();
        starts.push(pairs);
    }
    let mut check = 0i64;
    for p in 0..10i64 {
        for a in 0..10 {
            for j in 0..20 {
                let m = closest_meeting_node(&graphs[a], starts[a][2 * j], starts[a][2 * j + 1]);
                check = (check * 31 + m + 2 + p) % 1000000007;
            }
        }
    }
    println!("10 passes over 10 graphs of 10^5 nodes: checksum {}", check);
}
