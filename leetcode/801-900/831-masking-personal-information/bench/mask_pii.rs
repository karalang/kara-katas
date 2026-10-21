// Benchmark for #831: Masking Personal Information -- the ★ arm (by the rules).
//
// Mirrors mask_pii.kara: an email keeps its name's first and last letter,
// lowered, around five `*`, and its domain lowered; a phone number shows
// its last four digits and masks the country code, the digits before the
// last ten.

fn mask_pii(s: &str) -> String {
    match s.find('@') {
        Some(at) => {
            let lower = s.to_lowercase();
            format!("{}*****{}", &lower[0..1], &lower[at - 1..])
        }
        None => {
            let mut digits = String::new();
            for c in s.chars() {
                if c.is_ascii_digit() {
                    digits.push(c);
                }
            }
            let n = digits.len();
            let local = format!("***-***-{}", &digits[n - 4..]);
            if n == 10 {
                local
            } else {
                format!("+{}-{}", "*".repeat(n - 10), local)
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(seed: &mut i64) -> char {
    let r = next_random(seed) % 52;
    if r < 26 { (b'a' + r as u8) as char } else { (b'A' + (r - 26) as u8) as char }
}

fn main() {
    let count = 64i64;
    let rounds = 12000000i64;
    let separators = ['+', '-', '(', ')', ' '];
    let mut seed = 831i64;
    let mut strings: Vec<String> = Vec::new();
    for g in 0..count {
        let mut s = String::new();
        if g % 2 == 0 {
            for _ in 0..2 + next_random(&mut seed) % 19 {
                s.push(letter(&mut seed));
            }
            s.push('@');
            for _ in 0..1 + next_random(&mut seed) % 8 {
                s.push(letter(&mut seed));
            }
            s.push('.');
            for _ in 0..1 + next_random(&mut seed) % 8 {
                s.push(letter(&mut seed));
            }
        } else {
            for _ in 0..10 + next_random(&mut seed) % 4 {
                if next_random(&mut seed) % 3 == 0 {
                    s.push(separators[(next_random(&mut seed) % 5) as usize]);
                }
                s.push((b'0' + (next_random(&mut seed) % 10) as u8) as char);
            }
        }
        strings.push(s);
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for round in 0..rounds {
        let m = mask_pii(&strings[(round % count) as usize]);
        total += m.len() as i64;
        checksum = (checksum * 131 + m.as_bytes()[m.len() - 1] as i64) % 1000000007;
    }
    println!("{} rounds of {} strings: {} characters, checksum {}", rounds, count, total, checksum);
}
