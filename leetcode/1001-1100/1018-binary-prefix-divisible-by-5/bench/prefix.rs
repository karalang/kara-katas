// LeetCode #1018: Binary Prefix Divisible By 5 -- bench
// Mirrors prefix.kara; see ../README.md § Benchmarks.

fn prefixes_div_by5(nums: &[i64]) -> Vec<bool> {
    let mut answer = Vec::new();
    let mut r = 0;
    for &bit in nums {
        r = (r * 2 + bit) % 5;
        answer.push(r == 0);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let len: i64 = 2000000;
    let rounds: i64 = 50;
    let mut seed: i64 = 1018;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..len {
        nums.push(next_random(&mut seed) % 2);
    }
    let mut trues: i64 = 0;
    let mut sum: i64 = 0;
    for round in 0..rounds {
        let at = (round * 39989 % len) as usize;
        nums[at] = 1 - nums[at];
        let answer = prefixes_div_by5(&nums);
        for i in 0..answer.len() {
            if answer[i] {
                trues += 1;
                sum = (sum + i as i64) % 1000000007;
            }
        }
    }
    println!("{} rounds over {} bits: {} true, index sum {}", rounds, len, trues, sum);
}
