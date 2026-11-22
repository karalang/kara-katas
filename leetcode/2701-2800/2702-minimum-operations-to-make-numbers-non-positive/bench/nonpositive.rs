// LeetCode #2702: Minimum Operations to Make Numbers Non-positive -- the
// bench (nonpositive.kara in Rust): a binary search on the count, each
// trial summing the extra shares the numbers still above t * y need.

fn min_operations(nums: &[i64], x: i64, y: i64) -> i64 {
    let mut low: i64 = 0;
    let mut high = nums.iter().max().unwrap() / y + 1;
    while low < high {
        let t = (low + high) / 2;
        let mut need: i64 = 0;
        for &v in nums.iter() {
            if v > t * y {
                need += (v - t * y + x - y - 1) / (x - y);
                if need > t {
                    break;
                }
            }
        }
        if need <= t {
            high = t;
        } else {
            low = t + 1;
        }
    }
    low
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let arrays = 100;
    let n = 10000;
    let rounds = 5;
    let mut seed: i64 = 2702;
    let mut problems: Vec<(Vec<i64>, i64, i64)> = Vec::new();
    for _ in 0..arrays {
        let nums: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000000 + 1).collect();
        let y = next_random(&mut seed) % 1000 + 1;
        let x = y + wide(&mut seed) % 1000000 + 1;
        problems.push((nums, x, y));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, x, y) in problems.iter() {
            let t = min_operations(nums, *x, *y);
            sum += t;
            check = (check * 31 + t + r) % 1000000007;
        }
    }
    println!("{} arrays of {} numbers up to 1000000000, {} rounds: operations sum to {}, checksum {}", arrays, n, rounds, sum, check);
}
