// Benchmark workload — 3Sum Closest (LeetCode #16).
// Rust mirror of bench/three_sum_closest.kara. Same M/N/K, LCG generator,
// per-case target bag, sort + two-pointer body, and sink — see that file's
// header for the rationale.

fn three_sum_closest(nums: &[i64], target: i64) -> i64 {
    let mut s = nums.to_vec();
    s.sort_unstable();
    let n = s.len() as i64;
    let mut best: i64 = s[0] + s[1] + s[2];
    let mut i: i64 = 0;
    while i < n - 2 {
        let mut lo = i + 1;
        let mut hi = n - 1;
        while lo < hi {
            let sum = s[i as usize] + s[lo as usize] + s[hi as usize];
            if sum == target {
                return sum;
            }
            if (sum - target).abs() < (best - target).abs() {
                best = sum;
            }
            if sum < target {
                lo += 1;
            } else {
                hi -= 1;
            }
        }
        i += 1;
    }
    best
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
fn lcg_next(state: i64) -> i64 {
    (1103515245 * state + 12345) % 2147483648
}

fn build_case(seed: i64, count: i64) -> Vec<i64> {
    let mut v = Vec::with_capacity(count as usize);
    let mut state = seed;
    for _ in 0..count {
        state = lcg_next(state);
        v.push((state % 21) - 10);
    }
    v
}

fn target_for(idx: i64) -> i64 {
    match idx {
        0 => -12,
        1 => -6,
        2 => -1,
        3 => 0,
        4 => 1,
        5 => 5,
        6 => 11,
        _ => 19,
    }
}

fn main() {
    let m_cases: i64 = 8;
    let n_values: i64 = 16;
    let k_iters: i64 = 1_000_000;

    let sets: Vec<Vec<i64>> = (0..m_cases)
        .map(|m| build_case(m * 1000003 + 12345, n_values))
        .collect();

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let idx = k % m_cases;
        sum += three_sum_closest(&sets[idx as usize], target_for(idx));
    }
    println!("{}", sum);
}
