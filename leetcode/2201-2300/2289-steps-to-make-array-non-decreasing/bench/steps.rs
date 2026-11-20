// LeetCode #2289: Steps to Make Array Non-decreasing -- the bench, the ★
// arm in Rust. A stack of the elements still standing to the left, each
// with the step at which it is removed.

fn total_steps(nums: &[i64]) -> i64 {
    let mut stack: Vec<(i64, i64)> = Vec::new();
    let mut most = 0;
    for &x in nums {
        let mut step = 0;
        while !stack.is_empty() && stack[stack.len() - 1].0 <= x {
            step = step.max(stack[stack.len() - 1].1);
            stack.pop();
        }
        step = if stack.is_empty() { 0 } else { step + 1 };
        most = most.max(step);
        stack.push((x, step));
    }
    most
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2289;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..50 {
        let nums: Vec<i64> = (0..10000).map(|i| i * 3 + next_random(&mut seed) % 20000).collect();
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for _ in 0..20 {
        let mut total = 0;
        for nums in &arrays {
            total += total_steps(nums);
        }
        check = (check * 31 + total) % 1000000007;
    }
    println!("20 passes over 50 arrays of 10^4: checksum {}", check);
}
