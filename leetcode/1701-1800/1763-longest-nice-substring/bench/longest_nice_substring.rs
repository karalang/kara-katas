// LeetCode #1763: Longest Nice Substring -- the bench in Rust, mirroring
// longest_nice_substring.kara: divide and conquer at each letter whose
// other case is missing.
fn longest_nice_substring(s: &str) -> String {
    let bytes = s.as_bytes();
    for i in 0..bytes.len() {
        let c = bytes[i];
        let other = if c.is_ascii_lowercase() { c.to_ascii_uppercase() } else { c.to_ascii_lowercase() };
        if !bytes.contains(&other) {
            let left = longest_nice_substring(&s[..i].to_string());
            let right = longest_nice_substring(&s[i + 1..].to_string());
            return if right.len() > left.len() { right } else { left };
        }
    }
    s.to_string()
}

fn main() {
    let mut seed: i64 = 1763;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..1000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let letters = 1 + seed / 65536 % 12;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let upper = seed / 65536 % 101;
        let mut s = String::new();
        for _ in 0..100 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let base = if seed / 65536 % 100 < upper { 65 } else { 97 };
            seed = (seed * 1103515245 + 12345) % 2147483648;
            s.push(char::from_u32((base + seed / 65536 % letters) as u32).unwrap());
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..500000i64 {
        let s = &strings[((check + call * 7919) % 1000) as usize];
        check = (check * 31 + longest_nice_substring(s).len() as i64) % 1000000007;
    }
    println!("500000 calls over 1000 strings: checksum {}", check);
}
