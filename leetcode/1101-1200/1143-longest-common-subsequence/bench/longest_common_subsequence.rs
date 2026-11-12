// LeetCode #1143: Longest Common Subsequence -- the bench in Rust, the ★
// arm's algorithm.

fn longest_common_subsequence(text1: &str, text2: &str) -> i64 {
    let a: Vec<char> = text1.chars().collect();
    let b: Vec<char> = text2.chars().collect();
    let (m, n) = (a.len(), b.len());
    let mut best = vec![vec![0i64; n + 1]; m + 1];
    for i in 1..m + 1 {
        for j in 1..n + 1 {
            best[i][j] = if a[i - 1] == b[j - 1] {
                best[i - 1][j - 1] + 1
            } else {
                best[i - 1][j].max(best[i][j - 1])
            };
        }
    }
    best[m][n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcd".chars().collect();
    let mut seed = 1143;
    let mut texts: Vec<Vec<char>> = Vec::new();
    for _ in 0..20 {
        let t: Vec<char> = (0..1000).map(|_| letters[(next_random(&mut seed) % 4) as usize]).collect();
        texts.push(t);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..10 {
        for p in 0..10 {
            for t in [2 * p, 2 * p + 1] {
                let at = (next_random(&mut seed) % 1000) as usize;
                texts[t][at] = letters[(next_random(&mut seed) % 4) as usize];
            }
            let text1: String = texts[2 * p].iter().collect();
            let text2: String = texts[2 * p + 1].iter().collect();
            let answer = longest_common_subsequence(&text1, &text2);
            total += answer;
            check = (check * 131 + answer + 1) % 1000000007;
        }
    }
    println!("10 rounds over 10 pairs of 1000 letters: answers total {total}, checksum {check}");
}
