// LeetCode #1512: Number of Good Pairs -- the bench: 50 arrays of 200000
// numbers from 1 to 100 built once, then each counted four times by the
// ★ arm.

fn num_identical_pairs(nums: &[i64]) -> i64 {
    let mut seen = vec![0i64; 101];
    let mut pairs = 0;
    for &x in nums {
        pairs += seen[x as usize];
        seen[x as usize] += 1;
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1512;
    let arrays: Vec<Vec<i64>> = (0..50)
        .map(|_| (0..200000).map(|_| next_random(&mut seed) % 100 + 1).collect())
        .collect();
    let mut check: i64 = 0;
    for _ in 0..4 {
        for nums in &arrays {
            check = (check * 31 + num_identical_pairs(nums) + 1) % 1000000007;
        }
    }
    println!("200 counts over 50 arrays of 200000 numbers: checksum {}", check);
}
