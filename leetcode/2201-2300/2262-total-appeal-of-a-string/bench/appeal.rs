// LeetCode #2262: Total Appeal of A String -- Rust mirror of the ★ arm
// (appeal.kara): each position counts the substrings where its letter
// first appears, (i - last) * (n - i), with the last position kept per
// letter. Output is byte-identical to appeal.kara.

fn appeal_sum(s: &str) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len() as i64;
    let mut last = [-1i64; 26];
    let mut total = 0;
    for i in 0..n {
        let c = (bytes[i as usize] - b'a') as usize;
        total += (i - last[c]) * (n - i);
        last[c] = i;
    }
    total
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2262;
    let mut check = 0;
    for t in 0..40 {
        let letters = t % 26 + 1;
        let mut s = String::new();
        for _ in 0..100000 {
            s.push((b'a' + (next_random(&mut seed) % letters) as u8) as char);
        }
        check = (check * 31 + appeal_sum(&s)) % 1000000007;
    }
    println!("40 strings of 10^5: checksum {check}");
}
