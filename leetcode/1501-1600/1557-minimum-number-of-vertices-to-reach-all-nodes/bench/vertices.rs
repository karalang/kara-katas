// LeetCode #1557: Minimum Number of Vertices to Reach All Nodes -- bench:
// the ★ arm (the nodes no edge ends at) over 20 acyclic graphs of 100000
// nodes and up to 300000 edges, built once, each asked 20 times. Rust mirror of vertices.kara.

fn find_smallest_set_of_vertices(n: i64, edges: &[(i64, i64)]) -> Vec<i64> {
    let mut reached = vec![false; n as usize];
    for &(_, to) in edges {
        reached[to as usize] = true;
    }
    let mut sources = Vec::new();
    for v in 0..n {
        if !reached[v as usize] {
            sources.push(v);
        }
    }
    sources
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n = 100000i64;
    let mut seed = 1557i64;
    let mut graphs: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..20 {
        let mut order: Vec<i64> = (0..n).collect();
        for i in (1..n).rev() {
            let j = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (i + 1);
            order.swap(i as usize, j as usize);
        }
        let mut edges = Vec::new();
        for _ in 0..300000 {
            let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let b = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            if a < b {
                edges.push((order[a as usize], order[b as usize]));
            }
        }
        graphs.push(edges);
    }
    let mut check = 0i64;
    let mut total = 0usize;
    for pass in 0..20usize {
        for g in 0..graphs.len() {
            let sources = find_smallest_set_of_vertices(n, &graphs[g]);
            total += sources.len();
            check = mix(check, sources[(pass * 7 + g) % sources.len()]);
        }
    }
    println!("20 passes over 20 graphs of 100000 nodes: {} sources, checksum {}", total, check);
}
