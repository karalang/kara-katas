// LeetCode #1513: Number of Substrings With Only 1s -- the bench: 20
// strings of 500000 bits built once, then each counted five times by the
// ★ arm.

const MOD: i64 = 1000000007;

fn num_sub(s: &str) -> i64 {
    let mut run = 0i64;
    let mut total = 0i64;
    for c in s.chars() {
        if c == '1' {
            run += 1;
            total += run;
        } else {
            run = 0;
        }
    }
    total % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1513;
    let mut strings: Vec<String> = Vec::new();
    for k in 0..20 {
        let mut s = String::new();
        for _ in 0..500000 {
            s.push(if next_random(&mut seed) % 20 < k { '1' } else { '0' });
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for _ in 0..5 {
        for s in &strings {
            check = (check * 31 + num_sub(s) + 1) % 1000000007;
        }
    }
    println!("100 counts over 20 strings of 500000 bits: checksum {}", check);
}
