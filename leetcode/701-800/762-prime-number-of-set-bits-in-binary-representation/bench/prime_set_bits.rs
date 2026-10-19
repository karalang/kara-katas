// LeetCode 762 — Prime Number of Set Bits in Binary Representation:
// benchmark, the ★ arm in Rust.

fn count_prime_set_bits(left: i64, right: i64) -> i64 {
    let mut count = 0;
    for n in left..right + 1 {
        let mut bits = 0;
        let mut rest = n;
        while rest > 0 {
            rest &= rest - 1;
            bits += 1;
        }
        match bits {
            2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 => count += 1,
            _ => {}
        }
    }
    count
}

fn main() {
    let mut seed: i64 = 762;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds = 10000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let high = next_random();
        let left = 1 + (high * 32768 + next_random()) % 990000;
        let count = count_prime_set_bits(left, left + 10000);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    println!("{} ranges of 10001 numbers: {} counted, checksum {}", rounds, total, check);
}
