// Benchmark workload for LeetCode #259 — 3Sum Smaller (Rust mirror).
// Mirrors three_sum_smaller.kara algorithm-for-algorithm.

fn main() {
    let n: i64 = 4000;
    let rounds: i64 = 26;

    let mut base: Vec<i64> = Vec::with_capacity(n as usize);
    let mut state: i64 = 259259;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        base.push((state / 65536) % 2001 - 1000);
    }
    let mut probe = base.clone();
    probe.sort();
    let min_sum = probe[0] + probe[1] + probe[2];
    let max_sum = probe[(n - 1) as usize] + probe[(n - 2) as usize] + probe[(n - 3) as usize];
    let target = (min_sum + max_sum) / 2;

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let mut s = base.clone();
        s.sort();
        let mut count: i64 = 0;
        let mut a: i64 = 0;
        while a + 2 < n {
            let (mut lo, mut hi) = (a + 1, n - 1);
            while lo < hi {
                if s[a as usize] + s[lo as usize] + s[hi as usize] < target {
                    count += hi - lo;
                    lo += 1;
                } else {
                    hi -= 1;
                }
            }
            a += 1;
        }
        sink = (sink * 31 + count % 1000000007) % 1000000007;
    }
    println!("{}", sink);
}
