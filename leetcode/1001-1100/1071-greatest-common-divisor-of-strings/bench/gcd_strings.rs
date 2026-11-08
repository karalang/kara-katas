// LeetCode #1071: Greatest Common Divisor of Strings -- the benchmark's Rust
// mirror of gcd_strings.kara: the same concatenations compared over 20000
// pairs built once, each answered 50 times.

fn gcd(a: usize, b: usize) -> usize {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn gcd_of_strings(a: &str, b: &str) -> String {
    if a.to_string() + b != b.to_string() + a {
        return String::new();
    }
    a[..gcd(a.len(), b.len())].to_string()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: i64, k: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push((b'A' + (next_random(seed) % k) as u8) as char);
    }
    s
}

fn main() {
    let mut seed = 1071;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..20000 {
        let k = next_random(&mut seed) % 4 + 1;
        let root = random_word(next_random(&mut seed) % 20 + 1, k, &mut seed);
        let a = root.repeat((next_random(&mut seed) % 50 + 1) as usize);
        let mut b = root.repeat((next_random(&mut seed) % 50 + 1) as usize);
        let roll = next_random(&mut seed) % 6;
        if roll < 2 {
            let at = (next_random(&mut seed) % b.len() as i64) as usize;
            let letter = (b'A' + (next_random(&mut seed) % k) as u8) as char;
            b = format!("{}{}{}", &b[..at], letter, &b[at + 1..]);
        } else if roll == 2 {
            b = random_word(next_random(&mut seed) % 1000 + 1, k, &mut seed);
        }
        pairs.push((a, b));
    }
    let mut found = 0i64;
    let mut letters = 0i64;
    let mut check = 0i64;
    for _ in 0..50 {
        for (a, b) in pairs.iter() {
            let x = gcd_of_strings(a, b);
            if !x.is_empty() {
                found += 1;
            }
            letters += x.len() as i64;
            check = (check * 31 + x.len() as i64) % 1000000007;
        }
    }
    println!("1000000 calls: {found} found, {letters} letters, checksum {check}");
}
