// Benchmark for #483: Rust mirror of the ★ arm (the most 1s first, a
// float root); see smallest_good_base.kara.

fn is_ones(n: i64, k: i64, m: i64) -> bool {
    let mut sum = 1;
    let mut term = 1;
    for _ in 1..m {
        if term > (n - sum) / k {
            return false;
        }
        term *= k;
        sum += term;
    }
    sum == n
}

fn smallest_good_base(n: &str) -> String {
    let value: i64 = n.parse().unwrap();
    let mut m = 63;
    while m >= 3 {
        let root = (value as f64).powf(1.0 / (m - 1) as f64) as i64;
        for k in root..root + 2 {
            if k >= 2 && is_ones(value, k, m) {
                return format!("{k}");
            }
        }
        m -= 1;
    }
    format!("{}", value - 1)
}

fn main() {
    let count: i64 = 50000;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for i in 0..count {
        let mut n: i64 = 1000000000000000000 - 7 * i;
        if i % 3 == 2 {
            let k = 2 + i / 3;
            let m = 3 + (i / 3) % 6;
            n = 1;
            let mut term: i64 = 1;
            for _ in 1..m {
                if term > (1000000000000000000 - n) / k {
                    break;
                }
                term *= k;
                n += term;
            }
        }
        let base: i64 = smallest_good_base(&format!("{n}")).parse().unwrap();
        total += base % 1000;
        checksum = (checksum * 31 + base % 1000000007) % 1000000007;
    }
    println!("{count} values: bases add up to {total} (mod 1000 each), checksum {checksum}");
}
