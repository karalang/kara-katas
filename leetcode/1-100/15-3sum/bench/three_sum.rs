// Benchmark workload — 3Sum (LeetCode #15).
// Rust mirror of bench/three_sum.kara. Same M/N/K, LCG generator, sort +
// two-pointer dedup, and sink — see that file's header for the rationale.

fn three_sum(nums: &[i64]) -> Vec<Vec<i64>> {
    let mut s = nums.to_vec();
    s.sort_unstable();
    let n = s.len() as i64;
    let mut result: Vec<Vec<i64>> = Vec::new();
    let mut i: i64 = 0;
    while i < n - 2 {
        if i > 0 && s[i as usize] == s[(i - 1) as usize] {
            i += 1;
            continue;
        }
        if s[i as usize] > 0 {
            break;
        }
        let mut lo = i + 1;
        let mut hi = n - 1;
        while lo < hi {
            let sum = s[i as usize] + s[lo as usize] + s[hi as usize];
            if sum < 0 {
                lo += 1;
            } else if sum > 0 {
                hi -= 1;
            } else {
                result.push(vec![s[i as usize], s[lo as usize], s[hi as usize]]);
                lo += 1;
                hi -= 1;
                while lo < hi && s[lo as usize] == s[(lo - 1) as usize] {
                    lo += 1;
                }
                while lo < hi && s[hi as usize] == s[(hi + 1) as usize] {
                    hi -= 1;
                }
            }
        }
        i += 1;
    }
    result
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

fn main() {
    let m_cases: i64 = 8;
    let n_values: i64 = 16;
    let k_iters: i64 = 1_000_000;

    let sets: Vec<Vec<i64>> = (0..m_cases)
        .map(|m| build_case(m * 1000003 + 12345, n_values))
        .collect();

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let idx = (k % m_cases) as usize;
        let r = three_sum(&sets[idx]);
        sum += r.len() as i64;
    }
    println!("{}", sum);
}
