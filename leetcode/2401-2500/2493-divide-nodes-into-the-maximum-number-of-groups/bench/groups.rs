// LeetCode #2493: Divide Nodes Into the Maximum Number of Groups -- Rust
// mirror of the benchmark (groups.kara): the same graph, passes and
// checksum; a Vec of adjacency Vecs built on every ask, a breadth-first
// search from every node.
use std::collections::HashSet;

fn magnificent_sets(n: usize, edges: &[[usize; 2]]) -> i64 {
    let mut next: Vec<Vec<usize>> = vec![Vec::new(); n + 1];
    for e in edges {
        next[e[0]].push(e[1]);
        next[e[1]].push(e[0]);
    }
    let mut most = vec![0i64; n + 1];
    for start in 1..=n {
        let mut depth = vec![-1i64; n + 1];
        depth[start] = 0;
        let mut queue = vec![start];
        let mut head = 0;
        let mut least = start;
        let mut deepest = 0;
        while head < queue.len() {
            let node = queue[head];
            head += 1;
            least = least.min(node);
            deepest = deepest.max(depth[node]);
            for &other in &next[node] {
                if depth[other] == -1 {
                    depth[other] = depth[node] + 1;
                    queue.push(other);
                } else if depth[other] == depth[node] {
                    return -1;
                }
            }
        }
        most[least] = most[least].max(deepest + 1);
    }
    most.iter().sum()
}

fn main() {
    let n: i64 = 500;
    let passes: i64 = 38;
    let mut seed: i64 = 2493;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut side = vec![0i64; (n + 1) as usize];
    for v in 1..=n as usize {
        side[v] = next_random() % 2;
    }
    let mut taken: HashSet<i64> = HashSet::new();
    let mut edges: Vec<[usize; 2]> = Vec::new();
    for _ in 0..8000 {
        let a = next_random() % n + 1;
        let b = next_random() % n + 1;
        if a != b && side[a as usize] != side[b as usize] && taken.insert(a.min(b) * 1000 + a.max(b)) {
            edges.push([a as usize, b as usize]);
        }
    }
    let m = edges.len() as i64;
    let mut check: i64 = 0;
    for p in 0..passes {
        let asked = edges[..(m - check % 100) as usize].to_vec();
        check = (check * 31 + magnificent_sets(n as usize, &asked) + p) % 1000000007;
    }
    println!("{passes} passes over 500 nodes and {m} edges: checksum {check}");
}
