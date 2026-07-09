// Benchmark workload — Edit Distance (LeetCode #72).
// Rust mirror of bench/edit_distance.kara. Faithful to the kata's Vec-based DP:
// each DP row and each input string is a `Vec` built by pushing (grows by
// doubling), exactly as Kāra's `Vec.new()+push` does — NOT a fixed stack array —
// so the cross-language comparison measures the same growing-dynamic-array
// discipline. Rolling O(n)-space Levenshtein, K=400_000 iters over length-24
// pairs. Compiled with `rustc -O`. See ../README.md § Benchmarks.

fn edit_distance(a: &[u8], b: &[u8], m: usize, n: usize) -> i64 {
    let mut prev: Vec<i64> = Vec::new();
    for j in 0..=n {
        prev.push(j as i64);
    }
    for i in 1..=m {
        let mut cur: Vec<i64> = Vec::new();
        cur.push(i as i64);
        for j in 1..=n {
            if a[i - 1] == b[j - 1] {
                cur.push(prev[j - 1]);
            } else {
                let mut x = prev[j - 1];
                if prev[j] < x {
                    x = prev[j];
                }
                if cur[j - 1] < x {
                    x = cur[j - 1];
                }
                cur.push(1 + x);
            }
        }
        prev = cur;
    }
    prev[n]
}

fn main() {
    let total: i64 = 400_000;
    let modulus: i64 = 1_000_000_007;

    let mut acc: i64 = 0;
    for k in 0..total {
        let mut a: Vec<u8> = Vec::new();
        let mut b: Vec<u8> = Vec::new();
        for p in 0..24i64 {
            a.push(((p * 7 + k) % 4) as u8);
            b.push(((p * 5 + 2 * k) % 4) as u8);
        }
        let d = std::hint::black_box(edit_distance(&a, &b, 24, 24));
        acc = (acc * 131 + d) % modulus;
    }
    println!("{}", acc);
}
