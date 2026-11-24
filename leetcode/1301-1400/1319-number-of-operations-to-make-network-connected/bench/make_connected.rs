// LeetCode #1319 bench, Rust mirror of the Kāra bench: the ★ arm
// (union-find with halved paths and the smaller group hung under the
// larger) on 4 networks of 10^5 computers built once; then 25 passes, each
// moving one cable of every network to a pair chosen by the checksum so
// far, answering it and folding the answer plus the pass into the checksum.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut at = x;
    while parent[at as usize] != at {
        parent[at as usize] = parent[parent[at as usize] as usize];
        at = parent[at as usize];
    }
    at
}

fn make_connected(n: i64, connections: &[Vec<i64>]) -> i64 {
    if (connections.len() as i64) < n - 1 {
        return -1;
    }
    let mut parent: Vec<i64> = (0..n).collect();
    let mut size: Vec<i64> = vec![1; n as usize];
    let mut groups = n;
    for c in connections {
        let a = find(&mut parent, c[0]);
        let b = find(&mut parent, c[1]);
        if a != b {
            let (big, small) = if size[a as usize] >= size[b as usize] { (a, b) } else { (b, a) };
            parent[small as usize] = big;
            size[big as usize] += size[small as usize];
            groups -= 1;
        }
    }
    groups - 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64, k: i64) -> i64 {
    let hi = next_random(seed);
    (hi * 32768 + next_random(seed)) % k
}

fn main() {
    let n: i64 = 100000;
    let mut seed = 1319i64;
    let mut nets: Vec<Vec<Vec<i64>>> = Vec::new();
    for kind in 0..4 {
        let mut cables: Vec<Vec<i64>> = Vec::new();
        if kind == 1 {
            for i in 1..n {
                cables.push(vec![i - 1, i]);
            }
            for k in (1..cables.len()).rev() {
                let j = wide(&mut seed, k as i64 + 1) as usize;
                cables.swap(k, j);
            }
        } else if kind == 2 {
            for g in 0..n / 10 {
                for u in 0..10 {
                    cables.push(vec![10 * g + u, 10 * g + (u + 1) % 10]);
                }
            }
        } else {
            let m = if kind == 0 { n } else { n - 1 } as usize;
            while cables.len() < m {
                let u = wide(&mut seed, n);
                let v = wide(&mut seed, n);
                if u != v {
                    cables.push(vec![u, v]);
                }
            }
        }
        nets.push(cables);
    }
    let mut check: i64 = 0;
    for pass in 0..25i64 {
        for t in 0..4 {
            let cables = &mut nets[t];
            let m = cables.len() as i64;
            let u = check % n;
            let v = (u + 1 + (check / 7) % (n - 1)) % n;
            cables[(check % m) as usize] = vec![u, v];
            let got = make_connected(n, cables);
            check = (check * 31 + got + 1 + pass) % 1000000007;
        }
    }
    println!("25 passes over 4 networks of 10^5: checksum {}", check);
}
