// LeetCode #2375: Construct Smallest Number From DI String -- the bench,
// the ★ arm in Rust: the digits 1 to n + 1 pushed on a stack, emptied at
// every I and at the end, so each run of D's comes out falling.

fn smallest_number(pattern: &str) -> String {
    let p = pattern.as_bytes();
    let mut out: Vec<u8> = Vec::new();
    let mut stack: Vec<u8> = Vec::new();
    for i in 0..p.len() + 1 {
        stack.push(b'1' + i as u8);
        if i == p.len() || p[i] == b'I' {
            while let Some(d) = stack.pop() {
                out.push(d);
            }
        }
    }
    String::from_utf8(out).unwrap()
}

fn main() {
    // every pattern of 1 to 8 letters, 510 in all
    let mut patterns: Vec<String> = Vec::new();
    for n in 1..9 {
        for mask in 0..1u32 << n {
            let letters: Vec<u8> = (0..n).map(|i| if (mask >> i) & 1 == 1 { b'D' } else { b'I' }).collect();
            patterns.push(String::from_utf8(letters).unwrap());
        }
    }
    let mut check = 0i64;
    for p in 0..2000i64 {
        for pattern in &patterns {
            let number = smallest_number(pattern);
            for &b in number.as_bytes() {
                check = (check * 31 + (b - b'0') as i64 + p) % 1000000007;
            }
        }
    }
    println!("2000 passes over 510 patterns: checksum {}", check);
}
