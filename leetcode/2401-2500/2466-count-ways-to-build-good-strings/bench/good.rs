// LeetCode #2466: Count Ways To Build Good Strings -- the bench, the ★ arm
// in Rust: bottom-up counts in a `Vec`, each length's the sum of the
// counts one block back, and the counts from `low` to `high` summed.

const MOD: i64 = 1000000007;

fn count_good_strings(low: i64, high: i64, zero: i64, one: i64) -> i64 {
    let mut ways = vec![0i64; (high + 1) as usize];
    ways[0] = 1;
    let mut total = 0;
    for len in 1..high + 1 {
        let l = len as usize;
        if len >= zero {
            ways[l] = (ways[l] + ways[(len - zero) as usize]) % MOD;
        }
        if len >= one {
            ways[l] = (ways[l] + ways[(len - one) as usize]) % MOD;
        }
        if len >= low {
            total = (total + ways[l]) % MOD;
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 cases built once, `high` from 50000 to 10^5, `low` from 1 to
    // `high`, blocks of 1 to 20 no longer than `low`; then 28 passes,
    // each setting every case's zero block from the checksum so far, then
    // answering it and folding the answer plus the pass into the checksum
    let mut seed = 2466;
    let mut cases: Vec<(i64, i64, i64, i64)> = Vec::new();
    for _ in 0..20 {
        let high = 50000 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50001;
        let low = 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % high;
        let zero = 1 + next_random(&mut seed) % low.min(20);
        let one = 1 + next_random(&mut seed) % low.min(20);
        cases.push((low, high, zero, one));
    }
    let mut check = 0i64;
    for p in 0..28i64 {
        for a in 0..cases.len() {
            let (low, high, _, one) = cases[a];
            let zero = 1 + (check + a as i64) % low.min(20);
            cases[a] = (low, high, zero, one);
            check = (check * 31 + count_good_strings(low, high, zero, one) + p) % 1000000007;
        }
    }
    println!("28 passes over 20 cases up to 10^5: checksum {}", check);
}
