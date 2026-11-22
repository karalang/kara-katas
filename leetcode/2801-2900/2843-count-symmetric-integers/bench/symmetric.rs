// LeetCode #2843: Count Symmetric Integers -- the bench, mirrored from
// symmetric.kara: each number written out, its halves copied out and
// their digits summed.

fn symmetric(x: i64) -> bool {
    let text = x.to_string();
    let digits = text.as_bytes();
    let n = digits.len();
    if n % 2 == 1 {
        return false;
    }
    let half = |part: Vec<u8>| -> i64 { part.iter().map(|&d| (d - b'0') as i64).sum() };
    half(digits[..n / 2].to_vec()) == half(digits[n / 2..].to_vec())
}

fn count_symmetric_integers(low: i64, high: i64) -> i64 {
    (low..high + 1).filter(|&x| symmetric(x)).count() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 5000;
    let rounds = 2;
    let mut seed = 2843;
    let mut ranges: Vec<(i64, i64)> = Vec::new();
    for _ in 0..count {
        let a = next_random(&mut seed) % 10000 + 1;
        let b = next_random(&mut seed) % 10000 + 1;
        ranges.push((a.min(b), a.max(b)));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(low, high) in ranges.iter() {
            let got = count_symmetric_integers(low, high);
            total += got;
            check = (check * 31 + got + r) % 1000000007;
        }
    }
    println!("{count} ranges, {rounds} rounds: {total} in all, checksum {check}");
}
