// LeetCode #1745: Palindrome Partitioning IV -- the bench (palin.kara in
// Rust): a table of palindromes, then every pair of cuts.

fn check_partitioning(s: &str) -> bool {
    let b: Vec<u8> = s.bytes().collect();
    let n = b.len();
    let mut is: Vec<Vec<bool>> = vec![vec![false; n]; n];
    for i in (0..n).rev() {
        for j in i..n {
            is[i][j] = b[i] == b[j] && (j - i < 2 || is[i + 1][j - 1]);
        }
    }
    for i in 1..n - 1 {
        if is[0][i - 1] {
            for j in i..n - 1 {
                if is[i][j] && is[j + 1][n - 1] {
                    return true;
                }
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(seed: &mut i64) -> char {
    if next_random(seed) % 2 == 0 { 'a' } else { 'b' }
}

fn palindrome(n: i64, seed: &mut i64) -> String {
    let half: Vec<char> = (0..(n + 1) / 2).map(|_| letter(seed)).collect();
    let mut text: String = half.iter().collect();
    let back: String = half[..(n / 2) as usize].iter().rev().collect();
    text.push_str(&back);
    text
}

fn main() {
    let count = 20;
    let rounds: i64 = 5;
    let n: i64 = 2000;
    let mut seed: i64 = 1745;
    let mut strings: Vec<String> = Vec::new();
    for k in 0..count {
        if k % 2 == 0 {
            let a = next_random(&mut seed) % (n - 2) + 1;
            let b = next_random(&mut seed) % (n - a - 1) + 1;
            let first = palindrome(a, &mut seed);
            let second = palindrome(b, &mut seed);
            let third = palindrome(n - a - b, &mut seed);
            strings.push(format!("{}{}{}", first, second, third));
        } else {
            strings.push((0..n).map(|_| letter(&mut seed)).collect());
        }
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (k, s) in strings.iter().enumerate() {
            let bit = if check_partitioning(s) { 1 } else { 0 };
            yes += bit;
            check = (check * 3 + bit + k as i64 + r) % 1000000007;
        }
    }
    println!("{} strings of {} letters, {} rounds: {} split, checksum {}", count, n, rounds, yes, check);
}
