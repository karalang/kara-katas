// LeetCode #2396: Strictly Palindromic Number -- the bench, the ★ arm in
// Rust: every base tried, each base's digits taken into a list and
// checked from both ends.

fn palindrome_in_base(n: i64, b: i64) -> bool {
    let mut digits: Vec<i64> = Vec::new();
    let mut m = n;
    while m > 0 {
        digits.push(m % b);
        m /= b;
    }
    let (mut i, mut j) = (0usize, digits.len() - 1);
    while i < j {
        if digits[i] != digits[j] {
            return false;
        }
        i += 1;
        j -= 1;
    }
    true
}

fn is_strictly_palindromic(n: i64) -> bool {
    (2..n - 1).all(|b| palindrome_in_base(n, b))
}

fn main() {
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for n in 4..10001i64 {
        let count = (2..n - 1).filter(|&b| palindrome_in_base(n, b)).count() as i64;
        total += count;
        check = (check * 31 + count + is_strictly_palindromic(n) as i64) % 1000000007;
    }
    println!("every base of every n from 4 to 10000: checksum {}, {} palindromes", check, total);
}
