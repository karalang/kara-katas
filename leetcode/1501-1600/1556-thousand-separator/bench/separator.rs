// LeetCode #1556: Thousand Separator -- bench: the ★ arm (a dot before
// every digit whose distance from the end is a positive multiple of three)
// over 1000000 numbers below 2^31, each with its own count of 1 to 10
// digits, drawn once, each asked 3 times. Rust mirror of separator.kara.

fn thousand_separator(n: i64) -> String {
    let digits = n.to_string();
    let length = digits.len();
    let mut out = String::new();
    for (i, c) in digits.chars().enumerate() {
        if i > 0 && (length - i) % 3 == 0 {
            out.push('.');
        }
        out.push(c);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1556i64;
    let mut numbers = Vec::new();
    for _ in 0..1000000 {
        let digits = next_random(&mut seed) % 10 + 1;
        let mut top = 1i64;
        for _ in 0..digits {
            top *= 10;
        }
        let wide = (next_random(&mut seed) * 32768 + next_random(&mut seed)) * 32768 + next_random(&mut seed);
        numbers.push((wide % top).min(2147483647));
    }
    let mut check = 0i64;
    let mut length = 0usize;
    for _ in 0..3 {
        for &n in &numbers {
            let text = thousand_separator(n);
            length += text.len();
            for b in text.bytes() {
                check = (check * 31 + b as i64 + 1) % 1000000007;
            }
        }
    }
    println!("3 passes over 1000000 numbers: {} characters, checksum {}", length, check);
}
