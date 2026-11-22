// LeetCode #2834: Find the Minimum Possible Sum of a Beautiful Array --
// the bench, mirrored from sum.kara: two arithmetic series.

const MOD: i64 = 1000000007;

fn minimum_possible_sum(n: i64, target: i64) -> i64 {
    let low = n.min(target / 2);
    let high = n - low;
    let first = low * (low + 1) / 2;
    let rest = high * (2 * target + high - 1) / 2;
    (first + rest) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 1000000;
    let rounds = 20;
    let mut seed = 2834;
    let mut pairs: Vec<(i64, i64)> = Vec::new();
    for _ in 0..count {
        let n = wide(&mut seed) % 1000000000 + 1;
        pairs.push((n, wide(&mut seed) % 1000000000 + 1));
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(n, target) in pairs.iter() {
            check = (check * 31 + minimum_possible_sum(n, target) + r) % MOD;
        }
    }
    println!("{count} pairs, {rounds} rounds: checksum {check}");
}
