// LeetCode #728: Self Dividing Numbers -- each digit, by remainders.
// Benchmark mirror of the Kara star arm: peel each number's digits off
// with % 10 and / 10, stopping at a 0 or a digit that does not divide
// it, and collect the numbers that pass.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn self_dividing(n: i64) -> bool {
    let mut rest = n;
    while rest > 0 {
        let d = rest % 10;
        if d == 0 || n % d != 0 {
            return false;
        }
        rest /= 10;
    }
    true
}

fn self_dividing_numbers(left: i64, right: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    for n in left..right + 1 {
        if self_dividing(n) {
            out.push(n);
        }
    }
    out
}

fn main() {
    let mut seed: i64 = 728;
    let mut count = 0;
    let mut sum = 0;
    for _ in 0..40000 {
        let a = 1 + next_random(&mut seed) % 10000;
        let b = 1 + next_random(&mut seed) % 10000;
        let left = if a < b { a } else { b };
        let right = if a < b { b } else { a };
        let found = self_dividing_numbers(left, right);
        count += found.len();
        for n in found.iter() {
            sum += *n;
        }
    }
    println!("40000 random ranges: {} numbers, sum {}", count, sum);
}
