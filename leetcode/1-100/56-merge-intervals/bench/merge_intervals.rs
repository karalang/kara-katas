// Benchmark workload — Merge Intervals (LeetCode #56).
// Rust mirror of bench/merge_intervals.kara. Same M/N/K, LCG generator,
// per-case (start, end) shape, sort-by-first-component + sweep, and sink
// — see that file's header for the rationale.

fn merge_intervals(intervals: &[(i64, i64)]) -> Vec<(i64, i64)> {
    let mut s = intervals.to_vec();
    s.sort_by(|a, b| a.0.cmp(&b.0));
    let mut result: Vec<(i64, i64)> = Vec::new();
    if s.is_empty() {
        return result;
    }
    let (mut cur_start, mut cur_end) = s[0];
    for i in 1..s.len() {
        let (start_i, end_i) = s[i];
        if start_i <= cur_end {
            if end_i > cur_end {
                cur_end = end_i;
            }
        } else {
            result.push((cur_start, cur_end));
            cur_start = start_i;
            cur_end = end_i;
        }
    }
    result.push((cur_start, cur_end));
    result
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
fn lcg_next(state: i64) -> i64 {
    (1103515245 * state + 12345) % 2147483648
}

fn build_case(seed: i64, count: i64) -> Vec<(i64, i64)> {
    let mut v = Vec::with_capacity(count as usize);
    let mut state = seed;
    for _ in 0..count {
        state = lcg_next(state);
        let start = state % 51;
        state = lcg_next(state);
        let width = (state % 10) + 1;
        v.push((start, start + width));
    }
    v
}

fn main() {
    let m_cases: i64 = 8;
    let n_values: i64 = 16;
    let k_iters: i64 = 1_000_000;

    let sets: Vec<Vec<(i64, i64)>> = (0..m_cases)
        .map(|m| build_case(m * 1000003 + 12345, n_values))
        .collect();

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let idx = (k % m_cases) as usize;
        let r = merge_intervals(&sets[idx]);
        sum += r.len() as i64;
    }
    println!("{}", sum);
}
