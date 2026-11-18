// LeetCode #2316: Count Unreachable Pairs of Nodes in an Undirected
// Graph -- the bench, the ★ arm in Rust. Union-find with union by size
// and path halving, then each set's root, met in order, pairs its size
// with every node of the sets before it.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn count_pairs(n: i64, edges: &[(i64, i64)]) -> i64 {
    let mut parent: Vec<i64> = (0..n).collect();
    let mut size = vec![1i64; n as usize];
    for &(a, b) in edges {
        let mut ra = find(&mut parent, a);
        let mut rb = find(&mut parent, b);
        if ra != rb {
            if size[ra as usize] < size[rb as usize] {
                std::mem::swap(&mut ra, &mut rb);
            }
            parent[rb as usize] = ra;
            size[ra as usize] += size[rb as usize];
        }
    }
    let mut before = 0i64;
    let mut pairs = 0i64;
    for x in 0..n as usize {
        if parent[x] == x as i64 {
            pairs += size[x] * before;
            before += size[x];
        }
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 100000i64;
    let mut seed = 2316i64;
    let mut graphs: Vec<Vec<(i64, i64)>> = Vec::new();
    for g in 0..10i64 {
        let mut edges = Vec::new();
        for i in 1..n {
            if next_random(&mut seed) % (g + 3) != 0 {
                let j = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % i;
                edges.push((i, j));
            }
        }
        graphs.push(edges);
    }
    let mut check = 0i64;
    for p in 0..50 {
        for a in 0..10 {
            check = (check * 31 + count_pairs(n, &graphs[(a + p) % 10]) % 1000000007) % 1000000007;
        }
    }
    println!("50 passes over 10 graphs of 10^5 nodes: checksum {}", check);
}
