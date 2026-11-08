// LeetCode #1523: Count Odd Numbers in an Interval Range -- bench: the ★
// arm over 2000000 random intervals within 0 to 10^9, built once and
// answered 100 times, each pass summed.

fn count_odds(low: i64, high: i64) -> i64 {
    (high + 1) / 2 - low / 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let count = 2000000;
    let mut seed = 1523i64;
    let mut lows: Vec<i64> = Vec::new();
    let mut highs: Vec<i64> = Vec::new();
    for _ in 0..count {
        let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000001;
        let b = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000001;
        lows.push(a.min(b));
        highs.push(a.max(b));
    }
    let mut check = 0;
    for _ in 0..100 {
        let mut total = 0i64;
        for i in 0..count {
            total += count_odds(lows[i], highs[i]);
        }
        check = mix(check, total % 1000000007);
    }
    println!("100 passes over 2000000 intervals within 0 to 10^9: checksum {}", check);
}
