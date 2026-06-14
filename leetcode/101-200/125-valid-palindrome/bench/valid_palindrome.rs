// LeetCode #125 bench harness — Rust peer (rustc -O, single-thread).
//
// Same allocating filter-then-compare as the Kāra mirror: each pass builds a
// normalized Vec<u8> (alnum, lowercased) then checks symmetry. Sink = ITERS.

const ITERS: i64 = 3_000_000;

fn is_alnum(b: u8) -> bool {
    b.is_ascii_digit() || b.is_ascii_lowercase() || b.is_ascii_uppercase()
}

fn is_palindrome(s: &[u8]) -> bool {
    let mut clean: Vec<u8> = Vec::new();
    for &b in s {
        if is_alnum(b) {
            clean.push(b.to_ascii_lowercase());
        }
    }
    let m = clean.len();
    if m == 0 {
        return true;
    }
    let mut lo = 0usize;
    let mut hi = m - 1;
    while lo < hi {
        if clean[lo] != clean[hi] {
            return false;
        }
        lo += 1;
        hi -= 1;
    }
    true
}

fn main() {
    let input = "A man, a plan, a canal: Panama".repeat(8);
    let bytes = input.as_bytes();
    let mut sum: i64 = 0;
    for _ in 0..ITERS {
        sum += is_palindrome(bytes) as i64;
    }
    println!("{}", sum);
}
