// Benchmark workload — 4Sum (LeetCode #18).
// Rust mirror of bench/four_sum.kara. Same M/N/K, LCG generator, per-case
// target bag, sort + two-fix + two-pointer body with dedup and min/max
// prunes, and sink — see that file's header for the rationale.

fn four_sum(nums: &[i64], target: i64) -> Vec<Vec<i64>> {
    let mut s = nums.to_vec();
    s.sort_unstable();
    let n = s.len() as i64;
    let mut result: Vec<Vec<i64>> = Vec::new();
    let mut a: i64 = 0;
    while a < n - 3 {
        if a > 0 && s[a as usize] == s[(a - 1) as usize] {
            a += 1;
            continue;
        }
        if s[a as usize] + s[(a + 1) as usize] + s[(a + 2) as usize] + s[(a + 3) as usize] > target {
            break;
        }
        if s[a as usize] + s[(n - 1) as usize] + s[(n - 2) as usize] + s[(n - 3) as usize] < target {
            a += 1;
            continue;
        }
        let mut b = a + 1;
        while b < n - 2 {
            if b > a + 1 && s[b as usize] == s[(b - 1) as usize] {
                b += 1;
                continue;
            }
            if s[a as usize] + s[b as usize] + s[(b + 1) as usize] + s[(b + 2) as usize] > target {
                break;
            }
            if s[a as usize] + s[b as usize] + s[(n - 1) as usize] + s[(n - 2) as usize] < target {
                b += 1;
                continue;
            }
            let mut lo = b + 1;
            let mut hi = n - 1;
            while lo < hi {
                let sum = s[a as usize] + s[b as usize] + s[lo as usize] + s[hi as usize];
                if sum < target {
                    lo += 1;
                } else if sum > target {
                    hi -= 1;
                } else {
                    result.push(vec![
                        s[a as usize],
                        s[b as usize],
                        s[lo as usize],
                        s[hi as usize],
                    ]);
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
            b += 1;
        }
        a += 1;
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

fn target_for(idx: i64) -> i64 {
    match idx {
        0 => -20,
        1 => -8,
        2 => -3,
        3 => 0,
        4 => 2,
        5 => 6,
        6 => 12,
        _ => 24,
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
        let r = four_sum(&sets[idx as usize], target_for(idx));
        sum += r.len() as i64;
    }
    println!("{}", sum);
}
