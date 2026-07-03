// LeetCode #57 — rayon-parallel Rust mirror (par lane, insert_interval).
// Same linear three-phase insert as ../insert_interval.rs; the K=1M
// reduction runs across a rayon pool. Hand-tuned-parallel comparator for
// Kāra's auto-par. Sink matches the kara/rust/c/go mirrors.

fn insert_interval(intervals: &[(i64, i64)], new_interval: (i64, i64)) -> Vec<(i64, i64)> {
    let mut result: Vec<(i64, i64)> = Vec::new();
    let n = intervals.len();
    let (mut new_start, mut new_end) = new_interval;
    let mut i = 0usize;

    while i < n {
        let cur = intervals[i];
        if cur.1 >= new_start {
            break;
        }
        result.push(cur);
        i += 1;
    }
    while i < n {
        let cur = intervals[i];
        if cur.0 > new_end {
            break;
        }
        if cur.0 < new_start {
            new_start = cur.0;
        }
        if cur.1 > new_end {
            new_end = cur.1;
        }
        i += 1;
    }
    result.push((new_start, new_end));
    while i < n {
        result.push(intervals[i]);
        i += 1;
    }
    result
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
fn lcg_next(state: i64) -> i64 {
    (1103515245 * state + 12345) % 2147483648
}

fn build_case(seed: i64, count: i64) -> Vec<(i64, i64)> {
    let mut v = Vec::with_capacity(count as usize);
    let mut state = seed;
    let mut cursor: i64 = 0;
    for _ in 0..count {
        state = lcg_next(state);
        let gap = (state % 4) + 2;
        state = lcg_next(state);
        let width = (state % 6) + 1;
        let start = cursor + gap;
        let end = start + width;
        v.push((start, end));
        cursor = end;
    }
    v
}

fn pick_new(case: &[(i64, i64)], m: i64, count: i64) -> (i64, i64) {
    let half = count / 2;
    let mut st = lcg_next(m * 7919 + 101);
    let lo = st % half;
    st = lcg_next(st);
    let span = st % half;
    let mut hi = lo + 1 + span;
    if hi > count - 1 {
        hi = count - 1;
    }
    (case[lo as usize].0, case[hi as usize].1)
}

fn main() {
    use rayon::prelude::*;
    let m_cases: i64 = 8;
    let n_values: i64 = 16;
    let k_iters: i64 = 1_000_000;

    let sets: Vec<Vec<(i64, i64)>> = (0..m_cases)
        .map(|m| build_case(m * 1000003 + 12345, n_values))
        .collect();
    let news: Vec<(i64, i64)> = (0..m_cases)
        .map(|m| pick_new(&sets[m as usize], m, n_values))
        .collect();

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % m_cases) as usize;
            let r = insert_interval(&sets[idx], news[idx]);
            r.len() as i64
        })
        .sum();
    println!("{}", sum);
}
