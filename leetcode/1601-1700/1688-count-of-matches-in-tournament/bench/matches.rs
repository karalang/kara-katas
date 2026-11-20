// LeetCode #1688: Count of Matches in Tournament -- the bench's Rust mirror:
// the ★ arm on 500000 random n up to 10^9, all drawn first, each answered
// 40 times.

fn matches(n: i32) -> i32 {
    let mut teams = n;
    let mut played = 0;
    while teams > 1 {
        played += teams / 2;
        teams = (teams + 1) / 2;
    }
    played
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 500000;
    let rounds = 40;
    let mut seed = 1688;
    let mut values: Vec<i32> = Vec::new();
    for _ in 0..count {
        let hi = next_random(&mut seed);
        values.push(((hi * 32768 + next_random(&mut seed)) % 1000000000 + 1) as i32);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &n in values.iter() {
            let answer = matches(n) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} values of n, {rounds} rounds: {total} matches, checksum {check}");
}
