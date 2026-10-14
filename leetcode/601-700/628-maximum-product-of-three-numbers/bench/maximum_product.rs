// LeetCode #628: Maximum Product of Three Numbers -- Rust mirror of the
// Kāra bench.
//
// The ★ arm's one pass over the same inputs and rounds.

fn maximum_product(nums: &[i64]) -> i64 {
    let mut max1 = i64::MIN;
    let mut max2 = i64::MIN;
    let mut max3 = i64::MIN;
    let mut min1 = i64::MAX;
    let mut min2 = i64::MAX;
    for &v in nums {
        if v > max1 {
            max3 = max2;
            max2 = max1;
            max1 = v;
        } else if v > max2 {
            max3 = max2;
            max2 = v;
        } else if v > max3 {
            max3 = v;
        }
        if v < min1 {
            min2 = min1;
            min1 = v;
        } else if v < min2 {
            min2 = v;
        }
    }
    (max1 * max2 * max3).max(max1 * min1 * min2)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let inputs = 20;
    let rounds = 20000;
    let mut seed: i64 = 628;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..inputs {
        let spread = 1 + next_random(&mut seed) % 1000;
        let mut nums = Vec::new();
        for _ in 0..10000 {
            nums.push(next_random(&mut seed) % (2 * spread + 1) - spread);
        }
        all.push(nums);
    }
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let p = maximum_product(&all[(r * 7) % inputs]);
        checksum = (checksum * 31 + p % 1000000007 + 1000000007) % 1000000007;
    }
    println!("{} inputs, {} rounds: checksum {}", inputs, rounds, checksum);
}
