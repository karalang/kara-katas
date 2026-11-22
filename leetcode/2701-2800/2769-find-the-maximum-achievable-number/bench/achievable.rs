// LeetCode #2769: Find the Maximum Achievable Number -- the bench in
// Rust: the ★ arm over 10^6 random pairs, all drawn first, then each
// answered 50 times into a running checksum.

fn the_maximum_achievable_x(num: i64, t: i64) -> i64 {
    num + 2 * t
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000000;
    let rounds = 50;
    let mut seed: i64 = 2769;
    let mut nums: Vec<i64> = Vec::new();
    let mut ts: Vec<i64> = Vec::new();
    for _ in 0..count {
        nums.push(next_random(&mut seed) % 50 + 1);
        ts.push(next_random(&mut seed) % 50 + 1);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let x = the_maximum_achievable_x(nums[i], ts[i]);
            total += x;
            check = (check * 31 + x + r) % 1000000007;
        }
    }
    println!("{} pairs, {} rounds: answers sum to {}, checksum {}", count, rounds, total, check);
}
