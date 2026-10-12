// LeetCode #420: Strong Password Checker -- Rust mirror of
// strong_password.kara (count the runs by length mod 3).

fn strong_password_checker(password: &str) -> i64 {
    let bytes = password.as_bytes();
    let n = password.len() as i64;
    let (mut lower, mut upper, mut digit) = (0, 0, 0);
    for &b in bytes {
        if b.is_ascii_lowercase() {
            lower = 1;
        } else if b.is_ascii_uppercase() {
            upper = 1;
        } else if b.is_ascii_digit() {
            digit = 1;
        }
    }
    let missing = 3 - lower - upper - digit;
    let mut replace = 0;
    let mut zero_mod = 0;
    let mut one_mod = 0;
    let mut i = 0;
    while i < n {
        let mut j = i;
        while j < n && bytes[j as usize] == bytes[i as usize] {
            j += 1;
        }
        let run = j - i;
        if run >= 3 {
            replace += run / 3;
            if run % 3 == 0 {
                zero_mod += 1;
            } else if run % 3 == 1 {
                one_mod += 1;
            }
        }
        i = j;
    }
    if n < 6 {
        return missing.max(6 - n);
    }
    if n <= 20 {
        return missing.max(replace);
    }
    let delete = n - 20;
    let mut left = delete;
    let first = left.min(zero_mod);
    replace -= first;
    left -= first;
    let second = left.min(2 * one_mod);
    replace -= second / 2;
    left -= second;
    replace -= (left / 3).min(replace);
    delete + missing.max(replace)
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls = 10000000;
    let mut seed: i64 = 420;
    let pool = b"aAbB1.";
    let mut text = String::new();
    while text.len() < 1000000 {
        let pick = pool[(step(&mut seed) % 6) as usize];
        let run = 1 + step(&mut seed) % 6;
        for _ in 0..run {
            text.push(pick as char);
        }
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let length = 1 + step(&mut seed) % 50;
        let start = step(&mut seed) * 30 % (1000000 - length);
        let answer = strong_password_checker(&text[start as usize..(start + length) as usize]);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{calls} calls: total {total}, checksum {checksum}");
}
