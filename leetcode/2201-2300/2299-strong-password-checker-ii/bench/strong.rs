// LeetCode #2299: Strong Password Checker II -- the bench, the ★ arm in
// Rust. One pass over the letters: a `match` sets one of four flags, and
// the letter before must differ from each one.

fn strong_password_checker_ii(password: &str) -> bool {
    if password.len() < 8 {
        return false;
    }
    let (mut lower, mut upper, mut digit, mut special) = (false, false, false, false);
    let mut prev = ' ';
    for c in password.chars() {
        if c == prev {
            return false;
        }
        match c {
            'a'..='z' => lower = true,
            'A'..='Z' => upper = true,
            '0'..='9' => digit = true,
            '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(' | ')' | '-' | '+' => special = true,
            _ => {}
        }
        prev = c;
    }
    lower && upper && digit && special
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let kinds: Vec<Vec<char>> = [
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "0123456789",
        "!@#$%^&*()-+",
    ]
    .iter()
    .map(|k| k.chars().collect())
    .collect();
    let mut seed = 2299;
    let mut passwords: Vec<String> = Vec::new();
    for _ in 0..200000 {
        let n = next_random(&mut seed) % 13 + 8;
        let width = next_random(&mut seed) % 12 + 1;
        let mut s = String::new();
        for _ in 0..n {
            let kind = &kinds[(next_random(&mut seed) % 4) as usize];
            s.push(kind[(next_random(&mut seed) % width.min(kind.len() as i64)) as usize]);
        }
        passwords.push(s);
    }
    let count = passwords.len();
    let mut check: i64 = 0;
    for pass in 0..20 {
        for i in 0..count {
            let p = &passwords[(i + 7 * pass) % count];
            let v = if strong_password_checker_ii(p) { p.len() as i64 } else { 1 };
            check = (check * 31 + v) % 1000000007;
        }
    }
    println!("20 passes over 2 * 10^5 passwords: checksum {}", check);
}
