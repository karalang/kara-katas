// LeetCode #1616: Split Two Strings to Make Palindrome -- the bench in
// Rust, mirroring split.kara: two pointers, a from the front against b
// from the back as far as they agree, then whether the middle left over,
// of a or of b, is a palindrome by itself; then the roles swapped.

fn is_palindrome(s: &[u8], lo: i64, hi: i64) -> bool {
    let (mut i, mut j) = (lo, hi);
    while i < j {
        if s[i as usize] != s[j as usize] {
            return false;
        }
        i += 1;
        j -= 1;
    }
    true
}

fn joins(a: &[u8], b: &[u8]) -> bool {
    let (mut i, mut j) = (0i64, a.len() as i64 - 1);
    while i < j && a[i as usize] == b[j as usize] {
        i += 1;
        j -= 1;
    }
    is_palindrome(a, i, j) || is_palindrome(b, i, j)
}

fn check_palindrome_formation(a: &str, b: &str) -> bool {
    joins(a.as_bytes(), b.as_bytes()) || joins(b.as_bytes(), a.as_bytes())
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn pair(n: usize, seed: &mut i64) -> (String, String) {
    let mut a = Vec::with_capacity(n);
    let mut b = Vec::with_capacity(n);
    for _ in 0..n {
        a.push(b'a' + (next_random(seed) % 2) as u8);
        b.push(b'a' + (next_random(seed) % 2) as u8);
    }
    let k = (next_random(seed) * 32768 + next_random(seed)) as usize % (n / 2 + 1);
    for j in 0..k {
        b[n - 1 - j] = a[j];
    }
    for j in 0..(n - 2 * k) / 2 {
        b[n - k - 1 - j] = b[k + j];
    }
    if next_random(seed) % 2 == 0 {
        let i = (next_random(seed) * 32768 + next_random(seed)) as usize % n;
        b[i] = b'a' + (next_random(seed) % 2) as u8;
    }
    (String::from_utf8(a).unwrap(), String::from_utf8(b).unwrap())
}

fn main() {
    let mut seed = 1616;
    let pairs: Vec<(String, String)> = (0..10).map(|_| pair(500000, &mut seed)).collect();
    let (mut check, mut yes) = (0i64, 0i64);
    for (a, b) in &pairs {
        for _ in 0..30 {
            let answer = check_palindrome_formation(a, b);
            if answer {
                yes += 1;
            }
            check = mix(check, if answer { 1 } else { 0 });
        }
    }
    println!("10 pairs of 500000 letters from 2, each checked 30 times: {yes} split, checksum {check}");
}
