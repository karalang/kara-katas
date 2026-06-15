// LeetCode #32 bench — Rust (mirror of longest_valid_parentheses.kara).
//
// The index-stack longest-valid-parens, stack allocated FRESH per call (the
// apples-to-apples peer to Kāra's per-call Vec). Sliding window over a fixed
// pseudo-random parens buffer, folded into a checksum. `rustc -O` wraps on
// overflow; the bench also builds a `-C overflow-checks=on` variant to match
// Kāra's checked-by-default semantics (the LCG/window math stays well inside
// i64, so neither variant traps).

fn longest_valid_window(buf: &[u8], start: i64, w: i64) -> i64 {
    let mut stack: Vec<i64> = Vec::new();
    stack.push(-1);
    let mut best: i64 = 0;
    let mut i: i64 = 0;
    while i < w {
        if buf[(start + i) as usize] == b'(' {
            stack.push(i);
        } else {
            stack.pop();
            if stack.is_empty() {
                stack.push(i);
            } else {
                let top = stack[stack.len() - 1];
                let len = i - top;
                if len > best {
                    best = len;
                }
            }
        }
        i += 1;
    }
    best
}

fn main() {
    let big_l: i64 = 4096;
    let w: i64 = 2048;
    let total: i64 = 330000;
    let modulus: i64 = 1000000007;

    let mut buf: Vec<u8> = Vec::new();
    let mut x: i64 = 0x12345;
    let mut p: i64 = 0;
    while p < big_l {
        x = (x * 1103515245 + 12345) & 0x7fffffff;
        if (x & 1) == 0 {
            buf.push(b'(');
        } else {
            buf.push(b')');
        }
        p += 1;
    }

    let span = big_l - w + 1;
    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let start = (k * 7) % span;
        let r = longest_valid_window(&buf, start, w);
        acc = (acc + r) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
