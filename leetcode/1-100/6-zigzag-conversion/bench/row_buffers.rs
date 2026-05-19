// Benchmark workload — row-buffer Zigzag Conversion. Rust mirror of
// bench/row_buffers.kara. Same N, R, K, num_rows, same input pattern,
// same sink formula — see that file's header for the workload rationale
// and sink derivation.

fn convert_off(chars: &[char], off: usize, len: usize, num_rows: usize) -> Vec<char> {
    if num_rows <= 1 || num_rows >= len {
        // Pass-through; never fires at the bench's N=10000, num_rows=4
        // parameters. The explicit per-element push (rather than the
        // single-shot `to_vec()` over `chars[off..off+len]`) keeps the
        // per-iter shape comparable across the trio.
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

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let off = k % r_period;
        let result = convert_off(&chars, off, n, num_rows);
        let last = result.len() - 1;
        sum += result[0] as i64 + result[last] as i64;
    }
    println!("{}", sum);
}
