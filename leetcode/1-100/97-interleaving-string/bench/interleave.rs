// Benchmark workload for LeetCode #97 — 2D interleaving-string DP, Rust mirror.
const MOD: i64 = 1_000_000_007;

fn is_interleave(s1: &[u8], s2: &[u8], s3: &[u8]) -> bool {
    let (n, m) = (s1.len() as i64, s2.len() as i64);
    if n + m != s3.len() as i64 {
        return false;
    }
    let stride = m + 1;
    let mut dp = vec![false; ((n + 1) * stride) as usize];
    dp[0] = true;
    for j in 1..=m {
        dp[j as usize] = dp[(j - 1) as usize] && s2[(j - 1) as usize] == s3[(j - 1) as usize];
    }
    for i in 1..=n {
        dp[(i * stride) as usize] =
            dp[((i - 1) * stride) as usize] && s1[(i - 1) as usize] == s3[(i - 1) as usize];
        for j in 1..=m {
            let up = dp[((i - 1) * stride + j) as usize] && s1[(i - 1) as usize] == s3[(i + j - 1) as usize];
            let left = dp[(i * stride + j - 1) as usize] && s2[(j - 1) as usize] == s3[(i + j - 1) as usize];
            dp[(i * stride + j) as usize] = up || left;
        }
    }
    dp[(n * stride + m) as usize]
}

fn main() {
    let s1s: [&[u8]; 12] = [b"baacccbabbacacabbbcabbcc", b"abcababacbbacbcbccbcac", b"abbaabbabacbcaaccbbcbcca", b"bacaccbbaaacbaaaabaaaa", b"cbabaabcacccbccaabbbc", b"bacaacaccaccacabcbbcccb", b"aaaccbbbcbaabbbcabbbbabc", b"abbabbabcbcccaaacabbccbb", b"caccbacaaacabbbcccb", b"cccbacbaacbbbcbaaccbb", b"aacbcaccaabbaababcccbc", b"bbacbaabbabbaabccbacccaa"];
    let s2s: [&[u8]; 12] = [b"baabaabbbcaccbcaaaaa", b"cacccaaaccaaacccbcacabc", b"bbacbacccccbaabccaacc", b"ccbbaabcaacaccccbcccaca", b"abaaabbbbccbaaccca", b"babaaccaccbaaaacbcccc", b"bbacaaaabaabbabacbcb", b"ccbbabaaabaccababacacbbc", b"bbccaabcbabcbcacacbccacc", b"ccabccacabbbaabacbacb", b"babcaabacabcbbcacab", b"abbaacaabccbcaababbbbbc"];
    let s3s: [&[u8]; 12] = [b"baabcaabcacabbbabbcaccbacabccaaaaaabbbcabbcc", b"cabacccacbaaabaccacaaabbaccbccbcbccacbcacabcc", b"bbaabbaabcbabcacbccaccbbcaaabacccaaccbbcbccca", b"baccacccbbbaabaaabccabaacaccccbaacabaaaaccaca", b"acbababaaabbbbcacbcbaacccabccccacaabbbc", b"babbaacaaaccaccacccabccacabcabbcaccbaacbcccc", b"aaabbacacaacabbbaabbbacbabacbcbabbbcabbbbabc", b"cabbacbbbabbaaabaacbcbcacccabaaabacacbcbabcbccbb", b"bcbacccacababcacbabcaabccaaacabbcbcccccbacc", b"cccccbaabcbcacacacbabbbbcbbaabacbacbaaccbb", b"aabcabbccaaacbaccabacabbbcbacaabababcccbc", b"abbbbaaaccabaabcacbbbabcbaabaabbabbbcbcbaccccaa"];
    let mut acc: i64 = 1;
    for _ in 0..400_000 {
        let idx = (acc % 12) as usize;
        let ok = is_interleave(s1s[idx], s2s[idx], s3s[idx]);
        let bit: i64 = if ok { 1 } else { 0 };
        acc = (acc * 131 + bit + 1) % MOD;
    }
    println!("{}", acc);
}
