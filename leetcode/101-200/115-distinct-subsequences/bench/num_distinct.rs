// LeetCode #115 bench — distinct subsequences, Rust mirror (2-D DP, Vec<Vec<i64>>).
const MOD: i64 = 1000000007;
fn num_distinct(s: &[u8], t: &[u8]) -> i64 {
    let (m, n) = (s.len(), t.len());
    let mut dp = vec![vec![0i64; n + 1]; m + 1];
    for row in dp.iter_mut() { row[0] = 1; }
    for r in 1..=m {
        for c in 1..=n {
            let skip = dp[r - 1][c];
            dp[r][c] = if s[r - 1] == t[c - 1] { skip + dp[r - 1][c - 1] } else { skip };
        }
    }
    dp[m][n]
}
fn main() {
    let ss: [&[u8]; 8] = [b"abcabcabcabcabcabcabcabc", b"aabbccaabbccaabbccaabbcc", b"abababababababababababab", b"xyzxyzxyzxyzxyzxyzxyzxyz", b"aaabbbcccaaabbbcccaaabbb", b"cbacbacbacbacbacbacbacba", b"abcabcabcabcabcabcabcabc", b"aabbaabbaabbaabbaabbaabb"];
    let ts: [&[u8]; 8] = [b"abcabc", b"abcabc", b"ababa", b"xyzxy", b"abcab", b"cbacb", b"cba", b"abab"];
    let mut acc: i64 = 1;
    for _ in 0..400000i64 {
        let idx = (acc % 8) as usize;
        let c = num_distinct(ss[idx], ts[idx]);
        acc = (acc * 1000003 + c + 1) % MOD;
    }
    println!("{}", acc);
}
