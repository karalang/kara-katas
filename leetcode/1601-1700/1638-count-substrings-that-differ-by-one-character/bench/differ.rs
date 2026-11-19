// LeetCode #1638: Count Substrings That Differ by One Character -- the
// bench's Rust mirror: the ★ arm on 5000 random pairs of 100-letter words
// over the letters a to c, all drawn first.

fn count_substrings(s: &str, t: &str) -> i64 {
    let (a, b) = (s.as_bytes(), t.as_bytes());
    let (n, m) = (a.len(), b.len());
    let mut left = vec![vec![0i64; m + 1]; n + 1];
    for i in 0..n {
        for j in 0..m {
            if a[i] == b[j] {
                left[i + 1][j + 1] = left[i][j] + 1;
            }
        }
    }
    let mut right = vec![vec![0i64; m + 1]; n + 1];
    for i in (0..n).rev() {
        for j in (0..m).rev() {
            if a[i] == b[j] {
                right[i][j] = right[i + 1][j + 1] + 1;
            }
        }
    }
    let mut count = 0;
    for i in 0..n {
        for j in 0..m {
            if a[i] != b[j] {
                count += (left[i][j] + 1) * (right[i + 1][j + 1] + 1);
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64) -> String {
    let mut word = String::new();
    for _ in 0..100 {
        word.push((b'a' + (next_random(seed) % 3) as u8) as char);
    }
    word
}

fn main() {
    let mut seed: i64 = 1638;
    let mut pairs = Vec::new();
    for _ in 0..5000 {
        let s = random_word(&mut seed);
        let t = random_word(&mut seed);
        pairs.push((s, t));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (s, t) in &pairs {
        let count = count_substrings(s, t);
        total += count;
        check = (check * 31 + count + 1) % 1000000007;
    }
    println!("5000 pairs of 100 letters: counts sum to {}, checksum {}", total, check);
}
