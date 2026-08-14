// Benchmark workload for LeetCode #270 — Closest BST Value (Rust mirror).
// Mirrors bst_close.kara algorithm-for-algorithm, including the hand-written
// native absolute value (see that file for why hand-writing it was wrong).

fn main() {
    let n: i64 = 30000;
    let queries: i64 = 100000;
    let rounds: i64 = 22;

    let mut val: Vec<i64> = Vec::new();
    let mut left: Vec<i64> = Vec::new();
    let mut right: Vec<i64> = Vec::new();
    let mut state: i64 = 270270;

    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let hi = state / 65536;
        state = (state * 1103515245 + 12345) & 2147483647;
        let v = (hi * 32768 + state / 65536) % 1000000;
        if val.is_empty() {
            val.push(v); left.push(-1); right.push(-1);
        } else {
            let mut cur = 0i64;
            loop {
                if v < val[cur as usize] {
                    if left[cur as usize] < 0 {
                        val.push(v); left.push(-1); right.push(-1);
                        left[cur as usize] = val.len() as i64 - 1;
                        break;
                    }
                    cur = left[cur as usize];
                } else {
                    if right[cur as usize] < 0 {
                        val.push(v); left.push(-1); right.push(-1);
                        right[cur as usize] = val.len() as i64 - 1;
                        break;
                    }
                    cur = right[cur as usize];
                }
            }
        }
    }

    let mut targets: Vec<f64> = Vec::with_capacity(queries as usize);
    for _ in 0..queries {
        state = (state * 1103515245 + 12345) & 2147483647;
        let th = state / 65536;
        state = (state * 1103515245 + 12345) & 2147483647;
        let whole = (th * 32768 + state / 65536) % 1100000 - 50000;
        state = (state * 1103515245 + 12345) & 2147483647;
        let frac = ((state / 65536) % 1000) as f64 / 1000.0;
        targets.push(whole as f64 + frac);
    }

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        for t in 0..queries {
            let target = targets[t as usize];
            let mut best = val[0];
            let mut best_diff = (val[0] as f64 - target).abs();
            let mut cur = 0i64;
            while cur >= 0 {
                let v = val[cur as usize];
                let d = (v as f64 - target).abs();
                if d < best_diff || (d == best_diff && v < best) {
                    best = v;
                    best_diff = d;
                }
                cur = if (v as f64) < target { right[cur as usize] } else { left[cur as usize] };
            }
            sink = (sink * 31 + best) % 1000000007;
        }
    }

    println!("{}", sink);
}
