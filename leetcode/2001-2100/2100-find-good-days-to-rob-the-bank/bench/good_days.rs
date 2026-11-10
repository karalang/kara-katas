// LeetCode #2100: Find Good Days to Rob the Bank -- Rust mirror of the ★
// arm's benchmark (good_days.kara): the same 100 schedules of 10^5 days,
// the two runs counted in two passes.

fn good_days_to_rob_bank(security: &[i64], time: i64) -> Vec<i64> {
    let n = security.len();
    let mut before = vec![0i64; n];
    let mut after = vec![0i64; n];
    for i in 1..n {
        if security[i] <= security[i - 1] {
            before[i] = before[i - 1] + 1;
        }
    }
    for i in (0..n - 1).rev() {
        if security[i] <= security[i + 1] {
            after[i] = after[i + 1] + 1;
        }
    }
    (0..n).filter(|&i| before[i] >= time && after[i] >= time).map(|i| i as i64).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2100;
    let mut total = 0;
    let mut check: i64 = 0;
    for _ in 0..100 {
        let mut guards: i64 = 50000;
        let mut security: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            guards = (guards + next_random(&mut seed) % 3 - 1).clamp(0, 100000);
            security.push(guards);
        }
        let time = next_random(&mut seed) % 8;
        let good = good_days_to_rob_bank(&security, time);
        total += good.len();
        for &d in &good {
            check = (check * 31 + d + 1) % 1000000007;
        }
    }
    println!("100 answers: {total} good days, checksum {check}");
}
