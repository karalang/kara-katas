// LeetCode #2497: Maximum Star Sum of a Graph -- Rust mirror of the
// benchmark (star_sum.kara): the same graph, passes and checksum; a Vec of
// neighbours' values per node built on every ask, sorted and reversed.
use std::collections::HashSet;

fn max_star_sum(vals: &[i64], edges: &[[usize; 2]], k: i64) -> i64 {
    let n = vals.len();
    let mut beside: Vec<Vec<i64>> = vec![Vec::new(); n];
    for e in edges {
        beside[e[0]].push(vals[e[1]]);
        beside[e[1]].push(vals[e[0]]);
    }
    let mut best = i64::MIN;
    for centre in 0..n {
        beside[centre].sort();
        beside[centre].reverse();
        let mut sum = vals[centre];
        let mut taken = 0;
        for &value in &beside[centre] {
            if taken == k || value <= 0 {
                break;
            }
            sum += value;
            taken += 1;
        }
        best = best.max(sum);
    }
    best
}

fn main() {
    let n: i64 = 100000;
    let passes: i64 = 125;
    let mut seed: i64 = 2497;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut wide = || {
        let hi = next_random();
        hi * 32768 + next_random()
    };
    let mut vals: Vec<i64> = Vec::new();
    for _ in 0..n {
        vals.push(wide() % 20001 - 10000);
    }
    let mut taken: HashSet<i64> = HashSet::new();
    let mut edges: Vec<[usize; 2]> = Vec::new();
    for _ in 0..n {
        let a = wide() % n;
        let b = wide() % n;
        if a != b && taken.insert(a.min(b) * n + a.max(b)) {
            edges.push([a as usize, b as usize]);
        }
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        let at = (check % n) as usize;
        let was = vals[at];
        vals[at] = (check / n + p) % 20001 - 10000;
        let k = check % 50;
        check = (check * 31 + max_star_sum(&vals, &edges, k) + p) % 1000000007;
        vals[at] = was;
    }
    println!("{passes} passes over 10^5 nodes and {} edges: checksum {check}", edges.len());
}
