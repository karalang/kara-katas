// LeetCode #2180: Count Integers With Even Digit Sum -- the benchmark's
// Rust mirror of even_digits.kara.

fn count_even(num: i64) -> i64 {
    let mut count = 0i64;
    for x in 1..=num {
        let mut total = 0i64;
        let mut rest = x;
        while rest > 0 {
            total += rest % 10;
            rest /= 10;
        }
        if total % 2 == 0 {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2180i64;
    let mut check = 0i64;
    for _ in 0..200000 {
        let num = next_random(&mut seed) % 1000 + 1;
        check = (check * 31 + count_even(num)) % 1000000007;
    }
    println!("200000 solves: checksum {}", check);
}
