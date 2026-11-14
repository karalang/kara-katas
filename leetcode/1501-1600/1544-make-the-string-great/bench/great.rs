// LeetCode #1544: Make The String Great -- bench: the ★ arm (a stack of
// chars) over 1000 strings of 1 to 100 letters (the constraint's bound),
// each over its own first 1 to 3 letters in both cases, built once, each
// made great 500 times. Rust mirror of great.kara.

fn make_good(s: &str) -> String {
    let mut stack: Vec<char> = Vec::new();
    for c in s.chars() {
        match stack.last() {
            Some(&top) if top != c && top.to_ascii_lowercase() == c.to_ascii_lowercase() => {
                stack.pop();
            }
            _ => stack.push(c),
        }
    }
    stack.iter().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1544i64;
    let mut strings = Vec::new();
    for _ in 0..1000 {
        let n = next_random(&mut seed) % 100 + 1;
        let used = next_random(&mut seed) % 3 + 1;
        let mut s = String::new();
        for _ in 0..n {
            let base = if next_random(&mut seed) % 2 == 0 { b'a' } else { b'A' };
            s.push((base + (next_random(&mut seed) % used) as u8) as char);
        }
        strings.push(s);
    }
    let mut check = 0i64;
    let mut total = 0i64;
    for _ in 0..500 {
        for s in &strings {
            let great = make_good(s);
            total += great.len() as i64;
            check = mix(check, great.len() as i64);
        }
    }
    println!("500 passes over 1000 strings of up to 100 letters: {} letters kept, checksum {}", total, check);
}
