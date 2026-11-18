// LeetCode #2277: Closest Node to Path in Tree -- the bench, the ★ arm.

fn distances(n: usize, adj: &[Vec<usize>], from: usize) -> Vec<i64> {
    let mut dist = vec![-1i64; n];
    dist[from] = 0;
    let mut queue = vec![from];
    let mut head = 0;
    while head < queue.len() {
        let v = queue[head];
        head += 1;
        for &w in &adj[v] {
            if dist[w] < 0 {
                dist[w] = dist[v] + 1;
                queue.push(w);
            }
        }
    }
    dist
}

fn closest_node(n: usize, edges: &[Vec<usize>], query: &[Vec<usize>]) -> Vec<usize> {
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in edges {
        adj[e[0]].push(e[1]);
        adj[e[1]].push(e[0]);
    }
    let dist: Vec<Vec<i64>> = (0..n).map(|v| distances(n, &adj, v)).collect();
    let mut answer = Vec::new();
    for q in query {
        let (start, end, node) = (q[0], q[1], q[2]);
        let mut best = start;
        for u in 0..n {
            if dist[start][u] + dist[u][end] == dist[start][end] && dist[u][node] < dist[best][node] {
                best = u;
            }
        }
        answer.push(best);
    }
    answer
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2277;
    let mut check: i64 = 0;
    for _ in 0..50 {
        let mut edges: Vec<Vec<usize>> = Vec::new();
        for i in 1..1000 {
            edges.push(vec![i, (next_random(&mut seed) % i as i64) as usize]);
        }
        let mut query: Vec<Vec<usize>> = Vec::new();
        for _ in 0..1000 {
            let s = (next_random(&mut seed) % 1000) as usize;
            let e = (next_random(&mut seed) % 1000) as usize;
            let x = (next_random(&mut seed) % 1000) as usize;
            query.push(vec![s, e, x]);
        }
        for a in closest_node(1000, &edges, &query) {
            check = (check * 31 + a as i64) % 1000000007;
        }
    }
    println!("50 trees of 1000: checksum {check}");
}
