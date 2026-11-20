// LeetCode #1671: Minimum Number of Removals to Make Mountain Array -- the
// bench's Rust mirror: the ★ arm on 300 arrays of 1000 values up to 10^9,
// one raised above the rest, all drawn first.

fn minimum_mountain_removals(nums: &[i32]) -> i32 {
    let n = nums.len();
    let mut up = vec![1i64; n];
    let mut down = vec![1i64; n];
    for i in 0..n {
        for j in 0..i {
            if nums[j] < nums[i] {
                up[i] = up[i].max(up[j] + 1);
            }
        }
    }
    for i in (0..n).rev() {
        for j in i + 1..n {
            if nums[j] < nums[i] {
                down[i] = down[i].max(down[j] + 1);
            }
        }
    }
    let mut longest = 0;
    for i in 1..n - 1 {
        if up[i] > 1 && down[i] > 1 {
            longest = longest.max(up[i] + down[i] - 1);
        }
    }
    (n as i64 - longest) as i32
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 300;
    let n: i64 = 1000;
    let most: i64 = 1000000000;
    let mut seed: i64 = 1671;
    let mut all: Vec<Vec<i32>> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % most + 1) as i32);
        }
        let peak = (next_random(&mut seed) % (n - 2) + 1) as usize;
        nums[peak] = (most + 1) as i32;
        all.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for nums in &all {
        let removed = minimum_mountain_removals(nums) as i64;
        total += removed;
        check = (check * 31 + removed) % 1000000007;
    }
    println!("{} arrays of {} values: {} removals, checksum {}", arrays, n, total, check);
}
