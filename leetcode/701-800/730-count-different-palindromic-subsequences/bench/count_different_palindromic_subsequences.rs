// LeetCode #730: Count Different Palindromic Subsequences -- by
// interval, with the next and previous copy of the end letter.
// Benchmark mirror of the Kara star arm: the count for each interval
// from the ones inside it.

const M: i64 = 1000000007;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn count_palindromic_subsequences(s: &str) -> i64 {
    let b = s.as_bytes();
    let n = b.len();
    let mut next_same = vec![n as i64; n];
    let mut prev_same = vec![-1i64; n];
    let mut last = [-1i64; 4];
    for i in 0..n {
        let c = (b[i] - b'a') as usize;
        prev_same[i] = last[c];
        if last[c] >= 0 {
            next_same[last[c] as usize] = i as i64;
        }
        last[c] = i as i64;
    }
    let mut count: Vec<Vec<i64>> = vec![vec![0; n]; n];
    for i in (0..n).rev() {
        count[i][i] = 1;
        for j in i + 1..n {
            let inner = if i + 1 + 1 <= j { count[i + 1][j - 1] } else { 0 };
            let v;
            if b[i] != b[j] {
                v = count[i + 1][j] + count[i][j - 1] - inner;
            } else {
                let lo = next_same[i];
                let hi = prev_same[j];
                if lo > hi {
                    v = 2 * inner + 2;
                } else if lo == hi {
                    v = 2 * inner + 1;
                } else {
                    let twice = if lo + 1 <= hi - 1 { count[(lo + 1) as usize][(hi - 1) as usize] } else { 0 };
                    v = 2 * inner - twice;
                }
            }
            count[i][j] = ((v % M) + M) % M;
        }
    }
    count[0][n - 1]
}

fn main() {
    let mut seed: i64 = 730;
    let mut sum = 0;
    for _ in 0..200 {
        let mut s = String::new();
        for _ in 0..1000 {
            s.push((b'a' + (next_random(&mut seed) % 4) as u8) as char);
        }
        sum = (sum + count_palindromic_subsequences(&s)) % M;
    }
    println!("200 strings of 1000 letters: sum {}", sum);
}
