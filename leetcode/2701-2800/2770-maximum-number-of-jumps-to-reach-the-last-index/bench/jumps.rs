// LeetCode #2770: Maximum Number of Jumps to Reach the Last Index -- the
// bench in Rust: the ★ arm over 40 arrays of 1000 numbers, all drawn
// first, then each answered 5 times.

fn maximum_jumps(nums: &[i64], target: i64) -> i64 {
    let n = nums.len();
    let mut most = vec![-1i64; n];
    most[0] = 0;
    for j in 1..n {
        for i in 0..j {
            if most[i] >= 0 && (nums[j] - nums[i]).abs() <= target {
                most[j] = most[j].max(most[i] + 1);
            }
        }
    }
    most[n - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    (a * 32768 + b) * 32768 + next_random(seed)
}

fn main() {
    let count = 40;
    let rounds = 5;
    let mut seed: i64 = 2770;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..1000).map(|_| wide(&mut seed) % 2000000001 - 1000000000).collect();
        let target = wide(&mut seed) % 2000000001;
        cases.push((nums, target));
    }
    let mut reached: i64 = 0;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, target) in cases.iter() {
            let a = maximum_jumps(nums, *target);
            if a >= 0 {
                reached += 1;
                total += a;
            }
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    println!("{} arrays of 1000, {} rounds: {} reached, jumps sum to {}, checksum {}", count, rounds, reached, total, check);
}
