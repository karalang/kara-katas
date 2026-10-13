// Benchmark for #516: Rust mirror of the ★ arm (a table over
// substrings); see longest_palindrome_subseq.kara.

fn longest_palindrome_subseq(b: &[u8]) -> i64 {
    let n = b.len();
    let mut best: Vec<Vec<i64>> = vec![vec![0; n]; n];
    let mut i = n;
    while i > 0 {
        i -= 1;
        best[i][i] = 1;
        for j in i + 1..n {
            if b[i] == b[j] {
                best[i][j] = best[i + 1][j - 1] + 2;
            } else {
                best[i][j] = best[i + 1][j].max(best[i][j - 1]);
            }
        }
    }
    best[0][n - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 120 random strings of 1,000 letters (the problem's most), from the
    // first 4 or all 26 in turn, solved once each.
    let mut seed: i64 = 516;
    let strings = 120;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for t in 0..strings {
        let letters = if t % 2 == 0 { 4 } else { 26 };
        let mut s: Vec<u8> = Vec::new();
        for _ in 0..1000 {
            s.push(b'a' + (next_random(&mut seed) % letters) as u8);
        }
        let v = longest_palindrome_subseq(&s);
        total += v;
        checksum = (checksum * 31 + v) % 1000000007;
    }
    println!("{} strings of 1000 letters: {} in all, checksum {}", strings, total, checksum);
}
