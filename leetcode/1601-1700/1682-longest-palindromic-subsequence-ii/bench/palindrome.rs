// LeetCode #1682: Longest Palindromic Subsequence II -- the bench's Rust
// mirror: the ★ arm on 200 random strings of 250 letters from the first 4
// of the alphabet, all drawn first, each answered 2 times.

fn longest_palindrome_subseq(s: &str) -> i32 {
    let letters: Vec<i64> = s.bytes().map(|b| (b - b'a') as i64).collect();
    let n = letters.len();
    let mut best: Vec<Vec<[i32; 26]>> = vec![vec![[0; 26]; n]; n];
    for i in (0..n).rev() {
        for j in i + 1..n {
            for c in 0..26 {
                best[i][j][c] = if letters[i] == c as i64 && letters[j] == c as i64 {
                    let mut inside = 0;
                    if i + 1 < j - 1 {
                        for d in 0..26 {
                            if d != c {
                                inside = inside.max(best[i + 1][j - 1][d]);
                            }
                        }
                    }
                    inside + 2
                } else {
                    best[i + 1][j][c].max(best[i][j - 1][c])
                };
            }
        }
    }
    if n == 0 {
        return 0;
    }
    *best[0][n - 1].iter().max().unwrap()
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200;
    let n = 250;
    let rounds: i64 = 2;
    let alphabet = "abcd";
    let mut seed: i64 = 1682;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        for _ in 0..n {
            let at = (next_random(&mut seed) % 4) as usize;
            s.push_str(&alphabet[at..at + 1]);
        }
        strings.push(s);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in &strings {
            let answer = longest_palindrome_subseq(s) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} strings of {} letters, {} rounds: answers sum to {}, checksum {}", count, n, rounds, total, check);
}
