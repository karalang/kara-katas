// LeetCode #20 — rayon-parallel Rust mirror (par lane, valid_parentheses).
// Same byte-buffer build + stack-of-expected-closers validate as
// ../valid_parentheses.rs; the K=500k count-reduction runs across a rayon
// pool. Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches
// the kara/rust/c/go mirrors.

use rayon::prelude::*;

fn is_valid_bytes(bytes: &[u8]) -> bool {
    let mut stack: Vec<u8> = Vec::new();
    for &b in bytes {
        if b == b'(' || b == b'[' || b == b'{' {
            stack.push(match b {
                b'(' => b')',
                b'[' => b']',
                _ => b'}',
            });
        } else {
            match stack.pop() {
                Some(top) => {
                    if top != b {
                        return false;
                    }
                }
                None => return false,
            }
        }
    }
    stack.is_empty()
}

fn build_brackets(depth: i64, kind: i64, corrupt: bool) -> Vec<u8> {
    let (op, cl, wrong) = match kind {
        1 => (b'[', b']', b')'),
        2 => (b'{', b'}', b')'),
        _ => (b'(', b')', b']'),
    };
    let mut buf: Vec<u8> = Vec::new();
    for _ in 0..depth {
        buf.push(op);
    }
    for _ in 0..depth - 1 {
        buf.push(cl);
    }
    buf.push(if corrupt { wrong } else { cl });
    buf
}

fn main() {
    let depth: i64 = 1000;
    let k_iters: i64 = 500_000;

    let count: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let kind = k % 3;
            let corrupt = (k % 7) == 0;
            let buf = build_brackets(depth, kind, corrupt);
            if is_valid_bytes(&buf) {
                1
            } else {
                0
            }
        })
        .sum();
    println!("{}", count);
}
