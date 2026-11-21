// LeetCode #2411: Smallest Subarrays With Maximum Bitwise OR -- the bench,
// the ★ arm in Rust: walking from the right, the nearest index holding
// each of the 30 bits, the subarray from i reaching the farthest of them.

fn smallest_subarrays(nums: &[i64]) -> Vec<i64> {
    let n = nums.len();
    let mut nearest = vec![-1i64; 30];
    let mut answer = vec![1i64; n];
    for i in (0..n).rev() {
        let mut reach = i as i64;
        for bit in 0..30 {
            if nums[i] >> bit & 1 == 1 {
                nearest[bit] = i as i64;
            }
            reach = reach.max(nearest[bit]);
        }
        answer[i] = reach - i as i64 + 1;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2411;
    let arrays: Vec<Vec<i64>> = (0..5)
        .map(|i| (0..100000).map(|_| (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (1i64 << (6 * i + 6))).collect())
        .collect();
    let mut check: i64 = 0;
    for p in 0..10 {
        for nums in &arrays {
            for a in smallest_subarrays(nums) {
                check = (check * 31 + a + p) % 1000000007;
            }
        }
    }
    println!("10 passes over 5 arrays of 10^5 values: checksum {}", check);
}
