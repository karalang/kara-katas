// LeetCode 761 — Special Binary String: benchmark, the ★ arm in Rust.
// 200,000 random special strings of 50 characters.

fn make_largest_special(s: &str) -> String {
    let bytes = s.as_bytes();
    let mut mountains: Vec<String> = Vec::new();
    let mut depth = 0;
    let mut start = 0;
    for i in 0..bytes.len() {
        if bytes[i] == b'1' {
            depth += 1;
        } else {
            depth -= 1;
        }
        if depth == 0 {
            let inside = make_largest_special(&s[start + 1..i]);
            mountains.push(format!("1{}0", inside));
            start = i + 1;
        }
    }
    mountains.sort_by(|a, b| b.cmp(a));
    mountains.join("")
}

fn main() {
    let mut seed: i64 = 761;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds = 200000;
    let mut leading: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut s = String::with_capacity(50);
        let (mut ones, mut depth) = (0, 0);
        for _ in 0..50 {
            if ones < 25 && (depth == 0 || next_random() % 2 == 0) {
                s.push('1');
                ones += 1;
                depth += 1;
            } else {
                s.push('0');
                depth -= 1;
            }
        }
        let largest = make_largest_special(&s);
        let mut lead = true;
        for c in largest.bytes() {
            if c == b'0' {
                lead = false;
            }
            if lead {
                leading += 1;
            }
            check = (check * 2 + if c == b'1' { 1 } else { 0 }) % 1000000007;
        }
    }
    println!("{} strings of 50 characters: {} leading 1s, checksum {}", rounds, leading, check);
}
