// LeetCode #394 — rayon-parallel Rust mirror (par lane).
//
// Same iterative-stack decode as ../decode_string.rs, but the ITERS reduction
// runs across a rayon thread pool via `.into_par_iter().map(...).sum()`. This is
// the hand-tuned-parallel comparator for Kāra's auto-par: a Rust programmer
// must add the `rayon` crate and rewrite the loop into a parallel iterator;
// Kāra's compiler parallelizes the identical `sum += pass_len(...)` reduction
// with no source change. Same sink (41600000) as every other mirror.

use rayon::prelude::*;

const ENCODED: &str = "3[ab2[cd]ef]5[gh]2[ij3[kl]m]";
const ITERS: i64 = 800_000;

fn is_letter(b: u8) -> bool {
    b != b'[' && b != b']' && !b.is_ascii_digit()
}

fn decode_string(s: &str) -> String {
    let bytes = s.as_bytes();
    let n = bytes.len();
    let mut str_stack: Vec<String> = Vec::new();
    let mut num_stack: Vec<i64> = Vec::new();
    let mut cur = String::new();
    let mut k: i64 = 0;
    let mut i = 0;
    while i < n {
        let b = bytes[i];
        if b.is_ascii_digit() {
            k = k * 10 + (b - b'0') as i64;
            i += 1;
        } else if b == b'[' {
            str_stack.push(std::mem::take(&mut cur));
            num_stack.push(k);
            k = 0;
            i += 1;
        } else if b == b']' {
            let count = num_stack.pop().unwrap();
            let prev = str_stack.pop().unwrap();
            cur = prev + &cur.repeat(count.max(0) as usize);
            i += 1;
        } else {
            let mut j = i;
            while j < n && is_letter(bytes[j]) {
                j += 1;
            }
            cur.push_str(&s[i..j]);
            i = j;
        }
    }
    cur
}

fn main() {
    let sum: i64 = (0..ITERS)
        .into_par_iter()
        .map(|_| decode_string(ENCODED).len() as i64)
        .sum();
    println!("{}", sum);
}
