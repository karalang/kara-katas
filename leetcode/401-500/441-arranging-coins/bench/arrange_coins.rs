// Benchmark for #441: mirror of arrange_coins.kara (the closed form with
// an integer square root) on 3,000,000 random n up to 2^31 - 1.

// The largest r with r * r <= x.
fn isqrt(x: i64) -> i64 {
    if x < 2 {
        return x;
    }
    let mut r = x;
    let mut next = (r + x / r) / 2;
    while next < r {
        r = next;
        next = (r + x / r) / 2;
    }
    r
}

fn arrange_coins(n: i64) -> i64 {
    (isqrt(8 * n + 1) - 1) / 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 3000000;
    let mut seed: i64 = 441;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..count {
        let high = next_random(&mut seed) * 32768 + next_random(&mut seed);
        let n = 1 + (high * 2 + next_random(&mut seed) % 2) % 2147483647;
        let rows = arrange_coins(n);
        total += rows;
        checksum = (checksum * 31 + rows) % 1000000007;
    }
    println!("{} random n: total {}, checksum {}", count, total, checksum);
}
