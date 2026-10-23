// LeetCode #869: Reordered Power of 2 -- Rust mirror of the bench program
// (the ★ arm, digit counts), with the counts in a `Vec` as in the Kāra
// program.

fn digit_counts(x: i64) -> Vec<i64> {
    let mut counts = vec![0i64; 10];
    let mut rest = x;
    while rest > 0 {
        counts[(rest % 10) as usize] += 1;
        rest /= 10;
    }
    counts
}

fn reordered_power_of_2(n: i64) -> bool {
    let want = digit_counts(n);
    let mut power = 1;
    for _ in 0..30 {
        if digit_counts(power) == want {
            return true;
        }
        power *= 2;
    }
    false
}

fn main() {
    let limit: i64 = 1000000;
    let mut count: i64 = 0;
    let mut check: i64 = 0;
    for n in 1..=limit {
        if reordered_power_of_2(n) {
            count += 1;
            check = (check * 31 + n) % 1000000007;
        }
    }
    println!("n from 1 to {}: {} true, checksum {}", limit, count, check);
}
