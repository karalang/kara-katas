// LeetCode #906: Super Palindromes -- bench program, Rust.
//
// The palindromic roots built from their first halves, over random ranges
// below 10^18 given as strings. Each query counts the super-palindromes in
// its range and folds the count into a checksum.

fn superpalindromes_in_range(left: &str, right: &str) -> i64 {
    let lo: i64 = left.parse().unwrap();
    let hi: i64 = right.parse().unwrap();
    let mut count = 0;
    for odd in [true, false] {
        let mut half: i64 = 1;
        loop {
            let digits = half.to_string();
            let back: String = digits.chars().rev().collect();
            let tail = if odd { back[1..].to_string() } else { back };
            let root: i64 = (digits + &tail).parse().unwrap();
            if root > hi / root {
                break;
            }
            let square = root * root;
            let shown = square.to_string();
            let mirrored: String = shown.chars().rev().collect();
            if square >= lo && shown == mirrored {
                count += 1;
            }
            half += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let a = next_random(seed) * 32768 + next_random(seed);
    let b = next_random(seed) * 32768 + next_random(seed);
    a * 1073741824 + b
}

fn main() {
    let queries: i64 = 40;
    let top: i64 = 1000000000000000000;
    let mut seed: i64 = 906;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..queries {
        let a = 1 + big_random(&mut seed) % (top - 1);
        let b = 1 + big_random(&mut seed) % (top - 1);
        let got = superpalindromes_in_range(&a.min(b).to_string(), &a.max(b).to_string());
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    println!("{} ranges below 10^18: counts summing to {}, checksum {}", queries, total, check);
}
