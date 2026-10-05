// Benchmark workload for LeetCode #342 — Rust mirror of power_of_four.kara.

const LEN: i64 = 500000;
const PUNCHES: i64 = 100;
const MODULUS: i64 = 1073741789;
const I32_MIN: i64 = -2147483648;

fn is_power_of_four(n: i32) -> bool {
    n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn two_to(k: i64) -> i32 {
    let mut p: i32 = 1;
    for _ in 0..k {
        p *= 2;
    }
    p
}

fn value(seed: &mut i64) -> i32 {
    let kind = next(seed) % 3;
    if kind == 0 {
        return two_to(2 * (next(seed) % 16));
    }
    if kind == 1 {
        let r = next(seed) % 3;
        if r == 0 {
            return two_to(2 * (next(seed) % 15) + 1);
        }
        let p = two_to(2 * (next(seed) % 16));
        if r == 1 {
            return p + 1;
        }
        return p - 1;
    }
    let hi = next(seed) * 32768 + next(seed);
    (hi * 4 + next(seed) % 4 + I32_MIN) as i32
}

fn main() {
    let mut seed = 342;
    let mut a: Vec<i32> = Vec::new();
    for _ in 0..LEN {
        a.push(value(&mut seed));
    }
    let mut sink: i64 = 0;
    for _ in 0..PUNCHES {
        let pos = (next(&mut seed) * 32768 + next(&mut seed)) % LEN;
        a[pos as usize] = value(&mut seed);
        let mut count: i64 = 0;
        let mut sum: i64 = 0;
        for &x in &a {
            if is_power_of_four(x) {
                count += 1;
                sum += x as i64;
            }
        }
        sink = (sink * 31 + count + sum % MODULUS) % MODULUS;
    }
    println!("sink {}", sink);
}
