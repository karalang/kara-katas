// Benchmark for #829: Consecutive Numbers Sum -- the ★ arm (each length).
//
// Mirrors consecutive_numbers_sum.kara: n has a run of k consecutive
// numbers exactly when n - k * (k - 1) / 2 is a positive multiple of k,
// and k runs while 1 + 2 + ... + k fits.

fn consecutive_numbers_sum(n: i64) -> i64 {
    let mut count = 0;
    let mut k = 1i64;
    while k * (k + 1) / 2 <= n {
        if (n - k * (k - 1) / 2) % k == 0 {
            count += 1;
        }
        k += 1;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64i64;
    let rounds = 16000i64;
    let mut seed = 829i64;
    let mut numbers: Vec<i64> = Vec::new();
    for _ in 0..count {
        let a = next_random(&mut seed);
        let r = a * 32768 + next_random(&mut seed);
        numbers.push(500000000 + r % 500000001);
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for round in 0..rounds {
        let r = consecutive_numbers_sum(numbers[(round % count) as usize]);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    println!("{} rounds of {} numbers: total {}, checksum {}", rounds, count, total, checksum);
}
