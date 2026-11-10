// Benchmark: LeetCode #1092 Shortest Common Supersequence -- Rust mirror of
// the ★ arm: the longest common subsequence's table, a `Vec` of rows,
// walked back from the end. Same workload and sink as
// shortest_common_supersequence.kara.

fn shortest_common_supersequence(a: &str, b: &str) -> String {
    let x: Vec<char> = a.chars().collect();
    let y: Vec<char> = b.chars().collect();
    let (n, m) = (x.len(), y.len());
    let mut lcs = vec![vec![0i64; m + 1]; n + 1];
    for i in 1..=n {
        for j in 1..=m {
            lcs[i][j] = if x[i - 1] == y[j - 1] {
                lcs[i - 1][j - 1] + 1
            } else {
                lcs[i - 1][j].max(lcs[i][j - 1])
            };
        }
    }
    let mut out: Vec<char> = Vec::new();
    let (mut i, mut j) = (n, m);
    while i > 0 && j > 0 {
        if x[i - 1] == y[j - 1] {
            out.push(x[i - 1]);
            i -= 1;
            j -= 1;
        } else if lcs[i - 1][j] >= lcs[i][j - 1] {
            out.push(x[i - 1]);
            i -= 1;
        } else {
            out.push(y[j - 1]);
            j -= 1;
        }
    }
    while i > 0 {
        out.push(x[i - 1]);
        i -= 1;
    }
    while j > 0 {
        out.push(y[j - 1]);
        j -= 1;
    }
    out.iter().rev().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, len: i64, letters: i64) -> String {
    let mut w = String::new();
    for _ in 0..len {
        w.push(((97 + next_random(seed) % letters) as u8) as char);
    }
    w
}

fn main() {
    let mut seed = 1092i64;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for k in 0..50 {
        let letters = 2 + k % 25;
        let a = random_word(&mut seed, 1000, letters);
        let b = random_word(&mut seed, 1000, letters);
        pairs.push((a, b));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..4 {
        for (a, b) in pairs.iter() {
            let s: Vec<char> = shortest_common_supersequence(a, b).chars().collect();
            let len = s.len();
            total += len as i64;
            check = (check * 31 + len as i64) % 1000000007;
            check = (check * 31 + s[len / 3] as i64) % 1000000007;
            check = (check * 31 + s[2 * len / 3] as i64) % 1000000007;
        }
    }
    println!("4 rounds over 50 pairs of 1000 letters: lengths sum to {total}, checksum {check}");
}
