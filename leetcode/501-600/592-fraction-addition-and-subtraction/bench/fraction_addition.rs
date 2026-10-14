// Benchmark for #592: Rust mirror of the ★ arm (a running sum, reduced as
// it goes); see fraction_addition.kara. The expression is collected into
// a `Vec<char>` first, as the Kāra arm's is.

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a.abs() } else { gcd(b, a % b) }
}

fn digits(e: &[char], i: usize) -> (i64, usize) {
    let mut value = 0;
    let mut j = i;
    while j < e.len() && e[j].is_ascii_digit() {
        value = value * 10 + (e[j] as i64 - '0' as i64);
        j += 1;
    }
    (value, j)
}

fn fraction_addition(expression: &str) -> String {
    let e: Vec<char> = expression.chars().collect();
    let mut num: i64 = 0;
    let mut den: i64 = 1;
    let mut i = 0;
    while i < e.len() {
        let mut sign = 1;
        if e[i] == '-' || e[i] == '+' {
            if e[i] == '-' {
                sign = -1;
            }
            i += 1;
        }
        let (a, after_a) = digits(&e, i);
        let (b, after_b) = digits(&e, after_a + 1);
        i = after_b;
        let common = den / gcd(den, b) * b;
        num = num * (common / den) + sign * a * (common / b);
        den = common;
        let g = gcd(num, den);
        num /= g;
        den /= g;
    }
    format!("{}/{}", num, den)
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn coprime(a: i64, b: i64) -> bool {
    let (mut x, mut y) = (a, b);
    while y != 0 {
        let t = x % y;
        x = y;
        y = t;
    }
    x == 1
}

fn expression(count: i64, seed: &mut i64) -> String {
    let mut out = String::new();
    for k in 0..count {
        let mut a = 1 + step(seed) % 10;
        let mut b = 1 + step(seed) % 10;
        while !coprime(a, b) {
            a = 1 + step(seed) % 10;
            b = 1 + step(seed) % 10;
        }
        if step(seed) % 2 == 0 {
            out.push('-');
        } else if k > 0 {
            out.push('+');
        }
        out.push_str(&format!("{}/{}", a, b));
    }
    out
}

fn main() {
    let count = 1000;
    let rounds = 1000;
    let mut seed: i64 = 592;
    let mut expressions: Vec<String> = Vec::new();
    for _ in 0..count {
        expressions.push(expression(10, &mut seed));
    }
    let mut negative = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let got = fraction_addition(&expressions[(round * 7 + g) % count]);
            if got.starts_with('-') {
                negative += 1;
            }
            for c in got.chars() {
                checksum = (checksum * 31 + c as i64) % 1000000007;
            }
        }
    }
    println!("{} expressions, {} rounds: {} negative, checksum {}", count, rounds, negative, checksum);
}
