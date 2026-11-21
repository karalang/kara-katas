// LeetCode #2518: Number of Great Partitions -- Rust mirror of the
// benchmark (great.kara): the same lists, passes, order and checksum.

const MOD: i64 = 1000000007;

fn count_partitions(nums: &[i64], k: i64) -> i64 {
    let total: i64 = nums.iter().sum();
    if total < 2 * k {
        return 0;
    }
    let k = k as usize;
    let mut ways = vec![0i64; k];
    ways[0] = 1;
    let mut all = 1;
    for &x in nums {
        all = all * 2 % MOD;
        let x = x as usize;
        if x < k {
            for s in (x..k).rev() {
                ways[s] = (ways[s] + ways[s - x]) % MOD;
            }
        }
    }
    let short = ways.iter().fold(0, |a, &w| (a + w) % MOD);
    ((all - 2 * short) % MOD + MOD) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2518;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        lists.push((0..1000).map(|_| next_random(&mut seed) % 1000 + 1).collect());
    }
    let passes = 35;
    let mut check: i64 = 0;
    for p in 0..passes {
        for nums in lists.iter() {
            check = (check * 31 + count_partitions(nums, check % 1000 + 1) + p) % MOD;
        }
    }
    println!("{} passes over 20 lists of 1000 numbers: checksum {}", passes, check);
}
