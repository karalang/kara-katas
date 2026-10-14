// LeetCode 634 -- Find the Derangement of An Array, bench mirror in Rust.
//
// The ★ arm of find_derangement.kara: D(n) = (n - 1) * (D(n - 1) +
// D(n - 2)) modulo 10^9 + 7, kept in two variables. Same values of n,
// same output line.

const MOD: i64 = 1000000007;

fn find_derangement(n: i64) -> i64 {
    let mut before = 1;
    let mut last = 0;
    for i in 2..n + 1 {
        let next = (i - 1) * ((last + before) % MOD) % MOD;
        before = last;
        last = next;
    }
    last
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 634;
    let mut sizes: Vec<i64> = Vec::new();
    for _ in 0..100 {
        let wide = next_random(&mut seed) * 32768 + next_random(&mut seed);
        sizes.push(1 + wide % 1000000);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for &n in sizes.iter() {
        let d = find_derangement(n);
        total = (total + d) % MOD;
        checksum = (checksum * 31 + d) % MOD;
    }
    println!("{} values of n: total {}, checksum {}", sizes.len(), total, checksum);
}
