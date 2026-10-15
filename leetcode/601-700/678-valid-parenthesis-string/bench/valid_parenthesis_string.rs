// Benchmark for #678: the range of open counts, the ★ arm.

fn check_valid_string(s: &[u8]) -> bool {
    let mut low: i64 = 0;
    let mut high: i64 = 0;
    for &c in s {
        if c == b'(' {
            low += 1;
            high += 1;
        } else if c == b')' {
            low -= 1;
            high -= 1;
        } else {
            low -= 1;
            high += 1;
        }
        if high < 0 {
            return false;
        }
        if low < 0 {
            low = 0;
        }
    }
    low == 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_string(seed: &mut i64, c: i64) -> Vec<u8> {
    let mut s = Vec::new();
    if c % 3 == 0 {
        let n = 1 + next_random(seed) % 100;
        for _ in 0..n {
            let d = next_random(seed) % 3;
            s.push(if d == 0 { b'(' } else if d == 1 { b')' } else { b'*' });
        }
        return s;
    }
    let mut left = 1 + next_random(seed) % 50;
    let mut open = 0;
    let mut b = Vec::new();
    while left > 0 || open > 0 {
        if left > 0 && (open == 0 || next_random(seed) % 2 == 0) {
            b.push(b'(');
            open += 1;
            left -= 1;
        } else {
            b.push(b')');
            open -= 1;
        }
    }
    let stars = next_random(seed) % 4;
    let changes = next_random(seed) % 3;
    for &ch in &b {
        let r = next_random(seed) % 10;
        if r < stars {
            s.push(b'*');
        } else if r == 9 && next_random(seed) % 3 < changes {
            s.push(if ch == b'(' { b')' } else { b'(' });
        } else {
            s.push(ch);
        }
    }
    s
}

fn main() {
    let count: i64 = 20000;
    let rounds: i64 = 100;
    let mut seed: i64 = 678;
    let strings: Vec<Vec<u8>> = (0..count).map(|c| random_string(&mut seed, c)).collect();
    let mut sum: i64 = 0;
    let mut valid: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let k = ((i * 7919 + r * 104729) % count) as usize;
            let n = strings[k].len() as i64;
            if check_valid_string(&strings[k]) {
                valid += 1;
                sum = (sum * 31 + n) % 1000000007;
            } else {
                sum = (sum * 31 + 1000 + n) % 1000000007;
            }
        }
    }
    println!("{} rounds of {} strings: {} valid, checksum {}", rounds, count, valid, sum);
}
