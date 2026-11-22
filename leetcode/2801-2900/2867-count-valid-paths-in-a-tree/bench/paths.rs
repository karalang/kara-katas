// LeetCode #2867: Count Valid Paths in a Tree -- the bench, as
// paths.kara: 10 trees of 10^5 nodes, each answered 10 times by the
// disjoint-set arm.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut root = x;
    while parent[root as usize] != root {
        root = parent[root as usize];
    }
    let mut at = x;
    while parent[at as usize] != root {
        let next = parent[at as usize];
        parent[at as usize] = root;
        at = next;
    }
    root
}

fn count_paths(n: i64, edges: &[Vec<i64>]) -> i64 {
    let n = n as usize;
    let mut prime = vec![true; n + 1];
    prime[0] = false;
    prime[1] = false;
    let mut i = 2;
    while i * i <= n {
        if prime[i] {
            let mut j = i * i;
            while j <= n {
                prime[j] = false;
                j += i;
            }
        }
        i += 1;
    }
    let mut parent: Vec<i64> = (0..n as i64 + 1).collect();
    let mut size = vec![1i64; n + 1];
    let mut around: Vec<Vec<i64>> = vec![Vec::new(); n + 1];
    for e in edges {
        let (a, b) = (e[0], e[1]);
        if prime[a as usize] || prime[b as usize] {
            around[a as usize].push(b);
            around[b as usize].push(a);
        } else {
            let (ra, rb) = (find(&mut parent, a), find(&mut parent, b));
            if ra != rb {
                parent[ra as usize] = rb;
                size[rb as usize] += size[ra as usize];
            }
        }
    }
    let mut count = 0;
    for p in 2..n + 1 {
        if prime[p] {
            let mut before = 0;
            for &v in &around[p] {
                if !prime[v as usize] {
                    let s = size[find(&mut parent, v) as usize];
                    count += s + s * before;
                    before += s;
                }
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (10, 10, 100000i64);
    let mut seed = 2867;
    let mut trees: Vec<Vec<Vec<i64>>> = Vec::new();
    for c in 0..count {
        let mut edges: Vec<Vec<i64>> = Vec::new();
        for v in 2..n + 1 {
            let reach = if c % 2 == 1 { (v - 1).min(5) } else { v - 1 };
            edges.push(vec![v - 1 - wide(&mut seed) % reach, v]);
        }
        trees.push(edges);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for edges in trees.iter() {
            let paths = count_paths(n, edges);
            total += paths;
            check = (check * 31 + paths % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} trees of {n}, {rounds} rounds: {total} paths, checksum {check}");
}
