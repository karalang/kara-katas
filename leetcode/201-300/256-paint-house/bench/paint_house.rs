// Benchmark workload for LeetCode #256 — Paint House (Rust mirror).
// Mirrors paint_house.kara algorithm-for-algorithm.

#[inline]
fn min2(a: i64, b: i64) -> i64 { if a < b { a } else { b } }

fn main() {
    let n: i64 = 150000;
    let rounds: i64 = 800;

    let mut cost: Vec<(i64, i64, i64)> = Vec::with_capacity(n as usize);
    let mut state: i64 = 256256;
    let mut cheap: i64 = 0;
    let mut run_left: i64 = 0;
    for _ in 0..n {
        if run_left == 0 {
            state = (state * 1103515245 + 12345) & 2147483647;
            run_left = (state / 65536) % 9 + 2;
            state = (state * 1103515245 + 12345) & 2147483647;
            cheap = (state / 65536) % 3;
        }
        state = (state * 1103515245 + 12345) & 2147483647;
        let lo = (state / 65536) % 10 + 1;
        state = (state * 1103515245 + 12345) & 2147483647;
        let m1 = (state / 65536) % 40 + 40;
        state = (state * 1103515245 + 12345) & 2147483647;
        let m2 = (state / 65536) % 40 + 40;
        cost.push(if cheap == 0 { (lo, m1, m2) } else if cheap == 1 { (m1, lo, m2) } else { (m1, m2, lo) });
        run_left -= 1;
    }

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let (mut a, mut b, mut c) = cost[0];
        for k in 1..n as usize {
            let n_a = cost[k].0 + min2(b, c);
            let n_b = cost[k].1 + min2(a, c);
            let n_c = cost[k].2 + min2(a, b);
            a = n_a; b = n_b; c = n_c;
        }
        sink = (sink * 31 + min2(a, min2(b, c))) % 1000000007;
    }
    println!("{}", sink);
}
