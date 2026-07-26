// Benchmark harness for LeetCode #131 — Palindrome Partitioning.
// Mirrors palindrome_partitioning.kara algorithm-for-algorithm.
//
// `substring` walks the characters and filters, matching the kata's O(n)
// implementation rather than using Rust's O(1) `&s[lo..=hi]` slice. Using the
// native slice would make this lane a different algorithm — the per-piece cost
// is a real part of what the benchmark measures.

fn modulus() -> i64 {
    1000000007
}

fn is_pal(bytes: &[u8], lo: i64, hi: i64) -> bool {
    let mut l = lo;
    let mut h = hi;
    while l < h {
        if bytes[l as usize] != bytes[h as usize] {
            return false;
        }
        l += 1;
        h -= 1;
    }
    true
}

fn substring(s: &str, lo: i64, hi: i64) -> String {
    let mut out = String::new();
    for (i, ch) in s.chars().enumerate() {
        let i = i as i64;
        if i >= lo && i <= hi {
            out.push(ch);
        }
    }
    out
}

fn part_hash(path: &[String]) -> i64 {
    let m = modulus();
    let mut h: i64 = 0;
    for piece in path {
        for b in piece.bytes() {
            h = (h * 131 + (b as i64 - 96)) % m;
        }
        h = (h * 131 + 27) % m;
    }
    h
}

fn backtrack(
    s: &str,
    bytes: &[u8],
    start: i64,
    n: i64,
    path: &mut Vec<String>,
    count: &mut i64,
    digest: &mut i64,
) {
    if start == n {
        let m = modulus();
        *digest = (*digest + part_hash(path)) % m;
        *count += 1;
        return;
    }
    let mut end = start;
    while end < n {
        if is_pal(bytes, start, end) {
            path.push(substring(s, start, end));
            backtrack(s, bytes, end + 1, n, path, count, digest);
            path.pop();
        }
        end += 1;
    }
}

fn main() {
    let iters: i64 = 150;

    let cases = [
        "aaaaaaaaaaaaaaaa",
        "abababababababab",
        "abcdefghijklmnop",
        "aabaacaabaacaaba",
    ];

    let np = cases.len() as i64;
    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        let s = cases[idx];
        let bytes = s.as_bytes();
        let n = bytes.len() as i64;
        let mut path: Vec<String> = Vec::new();
        let mut count: i64 = 0;
        let mut digest: i64 = 0;
        backtrack(s, bytes, 0, n, &mut path, &mut count, &mut digest);
        sink = (sink + count * 7 + digest) % 1000000007;
    }
    println!("{}", sink);
}
