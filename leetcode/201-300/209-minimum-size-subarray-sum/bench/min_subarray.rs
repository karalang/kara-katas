// Benchmark workload for LeetCode #209 — Minimum Size Subarray Sum.
fn min_subarray_len(target: i64, nums: &[i64], n: i64) -> i64 {
    let mut left = 0i64;
    let mut sum = 0i64;
    let mut best = -1i64;
    let mut right = 0i64;
    while right < n {
        sum += nums[right as usize];
        while sum >= target {
            let len = right - left + 1;
            if best == -1 || len < best {
                best = len;
            }
            sum -= nums[left as usize];
            left += 1;
        }
        right += 1;
    }
    if best == -1 {
        0
    } else {
        best
    }
}

fn main() {
    let n: i64 = 200000;
    let targets: i64 = 290;

    let mut nums: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        nums.push(1 + state % 100); // 1..100, all positive
    }

    let mut sink: i64 = 0;
    for t in 0..targets {
        let target = 200 + t * 80;
        sink += min_subarray_len(target, &nums, n);
    }

    println!("{}", sink);
}
