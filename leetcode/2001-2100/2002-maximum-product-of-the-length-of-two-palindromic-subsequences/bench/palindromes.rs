// LeetCode #2002: Maximum Product of the Length of Two Palindromic
// Subsequences -- the benchmark, the same algorithm as palindromes.kara.

fn longest_palindrome(chars: &[u8]) -> i64 {
    let n = chars.len();
    if n == 0 {
        return 0;
    }
    let mut dp = vec![vec![0i64; n]; n];
    for i in (0..n).rev() {
        dp[i][i] = 1;
        for j in i + 1..n {
            dp[i][j] = if chars[i] == chars[j] {
                dp[i + 1][j - 1] + 2
            } else {
                dp[i + 1][j].max(dp[i][j - 1])
            };
        }
    }
    dp[0][n - 1]
}

fn max_product(s: &str) -> i64 {
    let b = s.as_bytes();
    let n = b.len();
    let mut best = 0;
    for mask in 1..(1usize << n) {
        let mut picked: Vec<u8> = Vec::new();
        let mut rest: Vec<u8> = Vec::new();
        for i in 0..n {
            if (mask >> i) & 1 == 1 {
                picked.push(b[i]);
            } else {
                rest.push(b[i]);
            }
        }
        let mut reversed = picked.clone();
        reversed.reverse();
        if picked == reversed {
            best = best.max(picked.len() as i64 * longest_palindrome(&rest));
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2002;
    let mut strings: Vec<String> = Vec::new();
    for a in 0..3000i64 {
        let mut s = String::new();
        for _ in 0..12 {
            s.push((97 + next_random(&mut seed) % (2 + a % 4)) as u8 as char);
        }
        strings.push(s);
    }
    let (mut sum, mut check) = (0i64, 0i64);
    for s in strings.iter() {
        let answer = max_product(s);
        sum += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    println!("{} strings: sum {}, checksum {}", strings.len(), sum, check);
}
