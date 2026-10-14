// Benchmark for #564: Rust mirror of the ★ arm (five candidates); see
// nearest_palindromic.kara.

fn mirrored(half: i64, length: i64) -> i64 {
    let text = half.to_string();
    let mut s = text.clone();
    let chars: Vec<char> = text.chars().collect();
    let mut i = (length / 2).min(chars.len() as i64) - 1;
    while i >= 0 {
        s.push(chars[i as usize]);
        i -= 1;
    }
    s.parse().unwrap()
}

fn nearest_palindromic(n: &str) -> String {
    let value: i64 = n.parse().unwrap();
    let length = n.len() as i64;
    let half: i64 = n[..((length + 1) / 2) as usize].parse().unwrap();
    let mut candidates = vec![10i64.pow((length - 1) as u32) - 1, 10i64.pow(length as u32) + 1];
    for h in [half - 1, half, half + 1] {
        candidates.push(mirrored(h, length));
    }
    let mut best: i64 = -1;
    for c in candidates {
        if c == value || c < 0 {
            continue;
        }
        let d = (c - value).abs();
        let bd = (best - value).abs();
        if best == -1 || d < bd || (d == bd && c < best) {
            best = c;
        }
    }
    best.to_string()
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_number(t: i64, seed: &mut i64) -> String {
    let length = 1 + step(seed) % 18;
    let mut digits: Vec<i64> = vec![1 + step(seed) % 9];
    for _ in 1..length {
        digits.push(step(seed) % 10);
    }
    if t % 3 == 1 {
        for i in 0..length / 2 {
            digits[(length - 1 - i) as usize] = digits[i as usize];
        }
    }
    let mut value: i64 = 0;
    for d in digits {
        value = value * 10 + d;
    }
    if t % 3 == 2 {
        value = 10i64.pow((length - 1) as u32) + step(seed) % 7 - 3;
        if value < 1 {
            value = 1;
        }
    }
    value.to_string()
}

fn main() {
    let count: i64 = 10000;
    let rounds: i64 = 300;
    let mut seed: i64 = 564;
    let mut numbers: Vec<String> = Vec::new();
    for t in 0..count {
        numbers.push(random_number(t, &mut seed));
    }
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let got: i64 = nearest_palindromic(&numbers[((round * 7 + g) % count) as usize]).parse().unwrap();
            checksum = (checksum * 31 + got % 1000000007) % 1000000007;
        }
    }
    println!("{} numbers, {} rounds: checksum {}", count, rounds, checksum);
}
