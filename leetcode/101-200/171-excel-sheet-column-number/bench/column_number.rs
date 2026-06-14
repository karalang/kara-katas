// LeetCode #171 bench harness — Rust peer (rustc -O, single-thread).
//
// Horner-fold bijective base-26 parse — same canonical algorithm as the Kāra
// mirror. Compute-bound (no per-parse allocation). A LEN=50000 distinct-title
// corpus (too many to tabulate) parsed round-robin keeps the parse from being
// hoisted/folded. Sink sums the parsed column numbers across K_ITERS.

const LEN: i64 = 50_000;
const K_ITERS: i64 = 100_000_000;
const LETTERS: &[u8; 26] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ";

fn to_title(mut num: i64) -> String {
    let mut bytes = Vec::new();
    while num > 0 {
        num -= 1;
        bytes.push(LETTERS[(num % 26) as usize]);
        num /= 26;
    }
    bytes.reverse();
    String::from_utf8(bytes).unwrap()
}

fn to_number(title: &str) -> i64 {
    let mut n: i64 = 0;
    for &b in title.as_bytes() {
        n = n * 26 + (b - b'A') as i64 + 1;
    }
    n
}

fn main() {
    let corpus: Vec<String> = (1..=LEN).map(to_title).collect();
    let mut sum: i64 = 0;
    for k in 0..K_ITERS {
        let idx = (k % LEN) as usize;
        sum += to_number(&corpus[idx]);
    }
    println!("{}", sum);
}
