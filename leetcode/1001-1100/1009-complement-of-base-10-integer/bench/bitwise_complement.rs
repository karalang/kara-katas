// LeetCode #1009 bench: the ★ arm (an all-ones mask) over 1,000,000 n
// below 10^9, of random lengths, drawn once; each of 50 rounds takes the
// complement of every n plus the round number and folds the round's sum
// into a checksum.

fn bitwise_complement(n: i64) -> i64 {
    let mut mask = 1;
    while mask < n {
        mask = mask * 2 + 1;
    }
    mask ^ n
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000000;
    let rounds = 50;
    let mut seed = 1009;
    let mut values: Vec<i64> = Vec::with_capacity(count);
    for _ in 0..count {
        let bits = 1 + next_random(&mut seed) % 30;
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        values.push(((hi * 32768 + lo) % (1i64 << bits)) % 999999000);
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        let mut sum: i64 = 0;
        for k in 0..count {
            sum += bitwise_complement(values[k] + r);
        }
        check = (check * 31 + sum) % 1000000007;
    }
    println!("{} rounds over {} values of n: checksum {}", rounds, count, check);
}
