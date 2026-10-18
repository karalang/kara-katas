// LeetCode #738: Monotone Increasing Digits -- one drop, then nines.
// Benchmark mirror of the Kara star arm: the digits in a Vec, the first
// place where a digit is larger than the next, a step back over equal
// digits before it, that digit lowered by one and every digit after it
// made a 9.

fn monotone_increasing_digits(n: i64) -> i64 {
    let mut digits: Vec<i64> = Vec::new();
    let mut x = n;
    while x > 0 {
        digits.push(x % 10);
        x /= 10;
    }
    digits.reverse();
    let mut i = 0;
    while i + 1 < digits.len() && digits[i] <= digits[i + 1] {
        i += 1;
    }
    if i + 1 < digits.len() {
        while i > 0 && digits[i - 1] == digits[i] {
            i -= 1;
        }
        digits[i] -= 1;
        for j in i + 1..digits.len() {
            digits[j] = 9;
        }
    }
    let mut out = 0;
    for d in digits.iter() {
        out = out * 10 + *d;
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 738;
    let mut total: i64 = 0;
    let mut kept = 0;
    for _ in 0..3000000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let n = (a * 32768 + b) % 1000000001;
        let m = monotone_increasing_digits(n);
        if m == n {
            kept += 1;
        }
        total += m;
    }
    println!("3000000 random numbers: {} already monotone, answers sum to {}", kept, total);
}
