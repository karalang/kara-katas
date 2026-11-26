// LeetCode #1771: Maximize Palindrome Length From Subsequences -- the bench
// in Rust, mirroring longest_palindrome.kara: the longest palindromic
// subsequence of every stretch of the two words joined.
fn longest_palindrome(word1: &str, word2: &str) -> i32 {
    let joined = format!("{}{}", word1, word2);
    let s = joined.as_bytes();
    let n = s.len();
    let split = word1.len();
    let mut dp = vec![vec![0i32; n]; n];
    let mut best = 0i32;
    for i in (0..n).rev() {
        dp[i][i] = 1;
        for j in i + 1..n {
            if s[i] == s[j] {
                dp[i][j] = dp[i + 1][j - 1] + 2;
                if i < split && j >= split {
                    best = best.max(dp[i][j]);
                }
            } else {
                dp[i][j] = dp[i + 1][j].max(dp[i][j - 1]);
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1771;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..100 {
        let letters = 2 + next_random(&mut seed) % 25;
        let s: String = (0..1000).map(|_| (97 + next_random(&mut seed) % letters) as u8 as char).collect();
        words.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..40i64 {
        let a = ((check + call * 7919) % 100) as usize;
        let b = ((check / 100 + call * 31 + 1) % 100) as usize;
        check = (check * 31 + longest_palindrome(&words[a], &words[b]) as i64) % 1000000007;
    }
    println!("40 calls over 100 words: checksum {}", check);
}
