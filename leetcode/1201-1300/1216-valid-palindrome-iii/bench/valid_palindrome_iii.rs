// LeetCode #1216: Valid Palindrome III -- the bench in Rust: the ★ arm
// (the longest palindromic subsequence, one row at a time) on the same 48
// strings of 1000 letters, each asked with k = 200, 400, 600 and 800.

fn is_valid_palindrome(s: &str, k: i64) -> bool {
    let b = s.as_bytes();
    let n = b.len();
    let mut row = vec![0i64; n];
    for i in (0..n).rev() {
        row[i] = 1;
        let mut diagonal = 0;
        for j in i + 1..n {
            let below = row[j];
            row[j] = if b[i] == b[j] { diagonal + 2 } else { row[j].max(row[j - 1]) };
            diagonal = below;
        }
    }
    n as i64 - row[n - 1] <= k
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1216;
    let alphabets = [2, 4, 8, 26];
    let mut texts = Vec::new();
    for t in 0..48 {
        let letters = alphabets[t % 4];
        let mut s = String::with_capacity(1000);
        for _ in 0..1000 {
            s.push((b'a' + (next_random(&mut seed) % letters) as u8) as char);
        }
        texts.push(s);
    }
    let mut check: i64 = 0;
    let mut yes = 0;
    for s in texts.iter() {
        for k in [200, 400, 600, 800] {
            let answer = is_valid_palindrome(s, k);
            if answer {
                yes += 1;
            }
            check = (check * 131 + if answer { 2 } else { 1 } + k) % 1000000007;
        }
    }
    println!("48 strings of 1000 letters, 4 budgets each: {} true, checksum {}", yes, check);
}
