// LeetCode #1782: Count Pairs Of Nodes -- the bench in Rust, mirroring
// count_pairs.kara: two pointers over the sorted degrees less the joined
// pairs.
use std::collections::HashMap;

fn count_pairs(n: i32, edges: &[Vec<i32>], queries: &[i32]) -> Vec<i32> {
    let mut degree = vec![0i32; n as usize + 1];
    let mut shared: HashMap<(i32, i32), i32> = HashMap::new();
    for e in edges {
        let (a, b) = (e[0].min(e[1]), e[0].max(e[1]));
        degree[a as usize] += 1;
        degree[b as usize] += 1;
        *shared.entry((a, b)).or_insert(0) += 1;
    }
    let mut sorted: Vec<i32> = degree[1..].to_vec();
    sorted.sort();
    let mut answers = Vec::new();
    for &q in queries {
        let mut count: i64 = 0;
        let (mut lo, mut hi) = (0usize, sorted.len() - 1);
        while lo < hi {
            if sorted[lo] + sorted[hi] > q {
                count += (hi - lo) as i64;
                hi -= 1;
            } else {
                lo += 1;
            }
        }
        for (&(a, b), &c) in &shared {
            let sum = degree[a as usize] + degree[b as usize];
            if sum > q && sum - c <= q {
                count -= 1;
            }
        }
        answers.push(count as i32);
    }
    answers
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1782;
    let mut graphs: Vec<Vec<Vec<i32>>> = Vec::new();
    for g in 0..10i64 {
        let span = 50 + g * 2216;
        let mut edges: Vec<Vec<i32>> = Vec::new();
        for _ in 0..100000 {
            let a = 1 + next_random(&mut seed) % span;
            let b = 1 + (a + next_random(&mut seed) % (span - 1)) % span;
            edges.push(vec![a as i32, b as i32]);
        }
        graphs.push(edges);
    }
    let mut check: i64 = 0;
    for g in 0..10i64 {
        let top = 400000 / (50 + g * 2216);
        let queries: Vec<i32> = (0..20i64).map(|k| ((check + k * 997) % top) as i32).collect();
        for a in count_pairs(20000, &graphs[g as usize], &queries) {
            check = (check * 31 + a as i64 + 1) % 1000000007;
        }
    }
    println!("10 graphs of 100000 edges: checksum {}", check);
}
