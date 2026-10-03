// Benchmark workload for LeetCode #335 — Rust mirror of self_crossing.kara.

const MOVES: i64 = 1000000;
const PUNCHES: i64 = 100;
const MODULUS: i64 = 1073741789;

fn is_self_crossing(d: &[i64]) -> bool {
    let n = d.len();
    for i in 3..n {
        if d[i] >= d[i - 2] && d[i - 1] <= d[i - 3] {
            return true;
        }
        if i >= 4 && d[i - 1] == d[i - 3] && d[i] + d[i - 4] >= d[i - 2] {
            return true;
        }
        if i >= 5
            && d[i - 2] >= d[i - 4]
            && d[i] + d[i - 4] >= d[i - 2]
            && d[i - 1] <= d[i - 3]
            && d[i - 1] + d[i - 5] >= d[i - 3]
        {
            return true;
        }
    }
    false
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next(seed);
    hi * 32768 + next(seed)
}

fn main() {
    let mut seed = 335i64;
    let mut d: Vec<i64> = Vec::new();
    for i in 0..MOVES as usize {
        let two_back = if i >= 2 { d[i - 2] } else { 0 };
        d.push(two_back + 1 + next(&mut seed) % 3);
    }
    let mut sink = 0i64;
    for p in 0..PUNCHES {
        let at = (2 + wide(&mut seed) % (MOVES - 2)) as usize;
        let old = d[at];
        if p % 2 == 0 {
            d[at] = 1;
        }
        let answer = if is_self_crossing(&d) { 1 } else { 0 };
        d[at] = old;
        sink = (sink * 1000003 + answer * 2000003 + at as i64) % MODULUS;
    }
    println!("{sink}");
}
