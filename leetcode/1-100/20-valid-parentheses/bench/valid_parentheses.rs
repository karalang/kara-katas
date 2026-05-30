// Benchmark workload — Valid Parentheses (LeetCode #20).
// Rust mirror of bench/valid_parentheses.kara. Same byte-buffer build +
// stack-of-expected-closers validate + count-valid sink, single-threaded.
// `Vec<u8>` grown from empty (no pre-reserve) mirrors Kāra's `Vec.new()`
// allocator traffic; the stack is a fresh `Vec<u8>` per call. Compiled
// with `rustc -O`. The seq lane's honest single-thread comparison.
// See ../README.md § Benchmarks.

use std::hint::black_box;

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

// `2*depth`-byte nested bracket buffer of the given kind; when `corrupt`,
// the final closer is flipped to a different closer type (invalid).
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

    let mut count: i64 = 0;
    for k in 0..k_iters {
        let kind = k % 3;
        let corrupt = (k % 7) == 0;
        let buf = build_brackets(depth, kind, corrupt);
        if is_valid_bytes(black_box(&buf)) {
            count += 1;
        }
    }
    println!("{}", count);
}
