// LeetCode 788 — Rotated Digits: the bench, in Rust.
// Mirrors rotated_digits.kara: every number up to n checked digit by
// digit, for 50,000 random n.

fn rotated_digits(n: i64) -> i64 {
    let mut good = 0;
    for x in 1..n + 1 {
        let mut rest = x;
        let mut valid = true;
        let mut changed = false;
        while rest > 0 {
            let d = rest % 10;
            if d == 3 || d == 4 || d == 7 {
                valid = false;
                break;
            }
            if d == 2 || d == 5 || d == 6 || d == 9 {
                changed = true;
            }
            rest /= 10;
        }
        if valid && changed {
            good += 1;
        }
    }
    good
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 788;
    let rounds = 50000;
    let mut sum = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let n = 1 + next_random(&mut seed) % 10000;
        let good = rotated_digits(n);
        sum += good;
        check = (check * 31 + good) % 1000000007;
    }
    println!("{rounds} rounds of n up to 10000: answers sum to {sum}, checksum {check}");
}
