// Benchmark for #410: mirror of split_array.kara (binary search on the
// answer).

fn pieces_needed(nums: &[i64], cap: i64) -> i64 {
    let mut pieces = 1;
    let mut sum = 0;
    for i in 0..nums.len() {
        if sum + nums[i] > cap {
            pieces += 1;
            sum = nums[i];
        } else {
            sum += nums[i];
        }
    }
    pieces
}

fn split_array(nums: &[i64], k: i64) -> i64 {
    let mut lo = 0;
    let mut hi = 0;
    for i in 0..nums.len() {
        if nums[i] > lo {
            lo = nums[i];
        }
        hi += nums[i];
    }
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if pieces_needed(nums, mid) <= k {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays: i64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(10000);
    let n = 1000;
    let mut seed: i64 = 410;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..arrays {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let hi = step(&mut seed);
            let lo = step(&mut seed);
            nums.push((hi * 32768 + lo) % 1000001);
        }
        let k = 1 + step(&mut seed) % 50;
        let answer = split_array(&nums, k);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{} arrays of {} numbers: total {}, checksum {}", arrays, n, total, checksum);
}
