// LeetCode #6 — rayon-parallel Rust mirror (par lane, row_buffers).
// Same row-buffer convert_off as ../row_buffers.rs; the K=10K reduction runs
// across a rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par.
// Sink matches the kara/rust/c/go mirrors.

fn convert_off(chars: &[char], off: usize, len: usize, num_rows: usize) -> Vec<char> {
    if num_rows <= 1 || num_rows >= len {
        let mut out: Vec<char> = Vec::with_capacity(len);
        for i in 0..len {
            out.push(chars[off + i]);
        }
        return out;
    }

    let mut rows: Vec<Vec<char>> = (0..num_rows).map(|_| Vec::new()).collect();
    let mut cur: usize = 0;
    let mut going_down = false;
    for i in 0..len {
        rows[cur].push(chars[off + i]);
        if cur == 0 || cur == num_rows - 1 {
            going_down = !going_down;
        }
        if going_down {
            cur += 1;
        } else {
            cur -= 1;
        }
    }

    let mut out: Vec<char> = Vec::with_capacity(len);
    for row in &rows {
        out.extend_from_slice(row);
    }
    out
}

fn main() {
    use rayon::prelude::*;
    let n: usize = 10_000;
    let r_period: usize = 1_000;
    let k_iters: usize = 10_000;
    let num_rows: usize = 4;

    let pattern: Vec<char> = "PAYPALISHIRING".chars().collect();
    let need = n + r_period;
    let mut chars: Vec<char> = Vec::with_capacity(need + pattern.len());
    while chars.len() < need {
        chars.extend(&pattern);
    }

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let off = k % r_period;
            let result = convert_off(&chars, off, n, num_rows);
            let last = result.len() - 1;
            result[0] as i64 + result[last] as i64
        })
        .sum();
    println!("{}", sum);
}
