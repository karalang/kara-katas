// LeetCode #2750: Ways to Split Array Into Good Subarrays -- the bench
// (splits.kara in Rust): the product of the distances between
// neighbouring 1s, mod 10^9 + 7.

const MOD: i64 = 1000000007;

fn number_of_good_subarray_splits(nums: &[i64]) -> i64 {
    let mut ways = 1;
    let mut last: Option<i64> = None;
    for (i, &x) in nums.iter().enumerate() {
        if x == 1 {
            if let Some(j) = last {
                ways = ways * (i as i64 - j) % MOD;
            }
            last = Some(i as i64);
        }
    }
    if last.is_none() { 0 } else { ways }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds = 20;
    let mut seed = 2750;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let percent = next_random(&mut seed) % 30 + 1;
        arrays.push((0..100000).map(|_| if next_random(&mut seed) % 100 < percent { 1 } else { 0 }).collect());
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let ways = number_of_good_subarray_splits(nums);
            sum += ways;
            check = (check * 31 + ways + r) % 1000000007;
        }
    }
    println!("{count} arrays of 100000, {rounds} rounds: ways sum to {sum}, checksum {check}");
}
