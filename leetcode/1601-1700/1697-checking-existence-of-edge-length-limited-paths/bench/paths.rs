// LeetCode #1697: Checking Existence of Edge Length Limited Paths -- the
// bench's Rust mirror: the ★ arm on 10 random graphs of 100000 nodes,
// 100000 edges and 100000 queries, lengths and limits up to 10^9, all
// drawn first, each answered 5 times.

fn find(parent: &mut [usize], x: usize) -> usize {
    let mut root = x;
    while parent[root] != root {
        root = parent[root];
    }
    let mut at = x;
    while parent[at] != root {
        let next = parent[at];
        parent[at] = root;
        at = next;
    }
    root
}

fn distance_limited_paths_exist(n: i32, edge_list: &[Vec<i32>], queries: &[Vec<i32>]) -> Vec<bool> {
    let mut edges = edge_list.to_vec();
    edges.sort_by_key(|e| e[2]);
    let mut order: Vec<usize> = (0..queries.len()).collect();
    order.sort_by_key(|&i| queries[i][2]);
    let mut parent: Vec<usize> = (0..n as usize).collect();
    let mut answer = vec![false; queries.len()];
    let mut joined = 0;
    for &i in order.iter() {
        let limit = queries[i][2];
        while joined < edges.len() && edges[joined][2] < limit {
            let a = find(&mut parent, edges[joined][0] as usize);
            let b = find(&mut parent, edges[joined][1] as usize);
            parent[a] = b;
            joined += 1;
        }
        answer[i] = find(&mut parent, queries[i][0] as usize) == find(&mut parent, queries[i][1] as usize);
    }
    answer
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(bound: i64, seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    (hi * 32768 + next_random(seed)) % bound
}

fn triples(count: i64, n: i64, seed: &mut i64) -> Vec<Vec<i32>> {
    let mut out = Vec::new();
    for _ in 0..count {
        let u = wide(n, seed);
        let v = (u + 1 + wide(n - 1, seed)) % n;
        out.push(vec![u as i32, v as i32, (wide(1000000000, seed) + 1) as i32]);
    }
    out
}

fn main() {
    let count = 10;
    let rounds = 5;
    let n: i64 = 100000;
    let mut seed = 1697;
    let mut graphs: Vec<(Vec<Vec<i32>>, Vec<Vec<i32>>)> = Vec::new();
    for _ in 0..count {
        let edges = triples(n, n, &mut seed);
        let queries = triples(n, n, &mut seed);
        graphs.push((edges, queries));
    }
    let mut trues: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (edges, queries) in graphs.iter() {
            let answer = distance_limited_paths_exist(n as i32, edges, queries);
            for &a in answer.iter() {
                if a {
                    trues += 1;
                }
                check = (check * 31 + if a { 2 } else { 1 } + r) % 1000000007;
            }
        }
    }
    println!("{count} graphs of {n} nodes, edges and queries, {rounds} rounds: {trues} true, checksum {check}");
}
