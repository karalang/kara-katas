// LeetCode #2779: Maximum Beauty of an Array After Applying Operation --
// the bench in Rust: the ★ arm over 20 arrays of 10^5 numbers, all drawn
// first, then each answered 10 times, every answer sorting its own copy.

fn maximum_beauty(nums: &[i64], k: i64) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let mut best = 0;
    let mut lo = 0;
    for hi in 0..sorted.len() {
        while sorted[hi] - sorted[lo] > 2 * k {
            lo += 1;
        }
        best = best.max(hi - lo + 1);
    }
    best as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 20;
    let rounds = 10;
    let mut seed: i64 = 2779;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..100000).map(|_| wide(&mut seed) % 100001).collect();
        let k = wide(&mut seed) % 1001;
        cases.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in cases.iter() {
            let b = maximum_beauty(nums, *k);
            total += b;
            check = (check * 31 + b + r) % 1000000007;
        }
    }
    println!("{} arrays of 10^5, {} rounds: beauties sum to {}, checksum {}", count, rounds, total, check);
}
