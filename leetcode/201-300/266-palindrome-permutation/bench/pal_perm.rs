// Benchmark workload for LeetCode #266 — Palindrome Permutation (Rust mirror).
// Mirrors pal_perm.kara algorithm-for-algorithm.

fn main() {
    let n: i64 = 200000;
    let rounds: i64 = 4000;
    let span: i64 = 1000;
    let width = n - span;

    let mut data: Vec<i64> = Vec::with_capacity(n as usize);
    let mut state: i64 = 266266;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        data.push(97 + (state / 65536) % 26);
    }

    let mut counts: Vec<i64> = vec![0; 256];

    let mut sink: i64 = 0;
    for r in 0..rounds {
        for c in 0..256 {
            counts[c] = 0;
        }

        let start = (r * 7919) % span;
        let stop = start + width;
        let mut i = start;
        while i < stop {
            let b = data[i as usize] as usize;
            counts[b] += 1;
            i += 1;
        }

        let mut odd: i64 = 0;
        for k in 0..256 {
            if counts[k] % 2 == 1 {
                odd += 1;
            }
        }
        let verdict: i64 = if odd <= 1 { 1 } else { 0 };
        sink = (sink * 131 + odd * 7 + verdict) % 1000000007;
    }

    println!("{}", sink);
}
