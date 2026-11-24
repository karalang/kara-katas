// LeetCode #1291 bench: the ★ arm over 10^5 ranges built once, then 20
// passes, each moving every range's low up by the checksum so far, answering
// it, and folding the count and the numbers found into the checksum.

fn sequential_digits(low: i64, high: i64) -> Vec<i64> {
    let mut found = Vec::new();
    for len in 2..10 {
        for first in 1..11 - len {
            let mut x = 0;
            for d in first..first + len {
                x = x * 10 + d;
            }
            if x >= low && x <= high {
                found.push(x);
            }
        }
    }
    found
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 1291;
    let mut ranges: Vec<(i64, i64)> = Vec::new();
    for _ in 0..100000 {
        let mut base = 10;
        for _ in 0..next_random(&mut seed) % 8 {
            base *= 10;
        }
        let mut span = 1;
        for _ in 0..next_random(&mut seed) % 10 {
            span *= 10;
        }
        let low = base + wide_random(&mut seed) % (9 * base);
        let high = low + wide_random(&mut seed) % span;
        ranges.push((low, high.min(1000000000)));
    }
    let mut check: i64 = 0;
    for p in 0..20 {
        for &(low, high) in ranges.iter() {
            let moved = low + check % 1000;
            let found = sequential_digits(moved.min(high), high);
            check = (check * 31 + found.len() as i64 + p) % 1000000007;
            for &x in found.iter() {
                check = (check * 131 + x) % 1000000007;
            }
        }
    }
    println!("20 passes over 10^5 ranges: checksum {}", check);
}
