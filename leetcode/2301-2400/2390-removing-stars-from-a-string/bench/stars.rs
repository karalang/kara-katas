// LeetCode #2390: Removing Stars From a String -- the bench, the ★ arm in
// Rust: a stack, a letter pushed and a star popping.

fn remove_stars(s: &str) -> String {
    let mut stack: Vec<u8> = Vec::new();
    for &b in s.as_bytes() {
        if b == b'*' {
            stack.pop();
        } else {
            stack.push(b);
        }
    }
    String::from_utf8(stack).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn starred(seed: &mut i64, len: i64, odds: i64) -> String {
    let mut out: Vec<u8> = Vec::new();
    let mut depth = 0;
    for _ in 0..len {
        if depth > 0 && next_random(seed) % odds == 0 {
            out.push(b'*');
            depth -= 1;
        } else {
            out.push(b'a' + (next_random(seed) % 26) as u8);
            depth += 1;
        }
    }
    String::from_utf8(out).unwrap()
}

fn main() {
    let mut seed = 2390i64;
    let strings: Vec<String> = (0..20).map(|_| starred(&mut seed, 100000, 3)).collect();
    let mut check = 0i64;
    for p in 0..100i64 {
        for s in &strings {
            let t = remove_stars(s);
            for &b in t.as_bytes() {
                check = (check * 31 + (b - b'a' + 1) as i64) % 1000000007;
            }
            check = (check * 31 + t.len() as i64 + p) % 1000000007;
        }
    }
    println!("100 passes over 20 strings of 10^5 characters: checksum {}", check);
}
