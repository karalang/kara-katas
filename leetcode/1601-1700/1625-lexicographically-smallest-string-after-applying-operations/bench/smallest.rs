// LeetCode #1625: Lexicographically Smallest String After Applying
// Operations -- the bench in Rust, mirroring smallest.kara: every rotation
// by a multiple of gcd(b, n) with every count of additions, each string
// made and the least kept.

fn gcd(x: i64, y: i64) -> i64 {
    if y == 0 { x } else { gcd(y, x % y) }
}

fn find_lex_smallest_string(s: &str, a: i32, b: i32) -> String {
    let digits: Vec<i64> = s.chars().map(|c| c as i64 - '0' as i64).collect();
    let n = digits.len();
    let step = gcd(b as i64, n as i64) as usize;
    let even_counts = if b % 2 == 1 { 10 } else { 1 };
    let mut best = s.to_string();
    for start in (0..n).step_by(step) {
        for odd in 0..10i64 {
            for even in 0..even_counts {
                let mut t = String::new();
                for i in 0..n {
                    let count = if i % 2 == 1 { odd } else { even };
                    let d = (digits[(i + start) % n] + count * a as i64) % 10;
                    t.push((b'0' + d as u8) as char);
                }
                if t < best {
                    best = t;
                }
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1625;
    let mut cases: Vec<(String, i32, i32)> = Vec::new();
    for _ in 0..200 {
        let mut s = String::new();
        for _ in 0..100 {
            s.push((b'0' + (next_random(&mut seed) % 10) as u8) as char);
        }
        let a = (next_random(&mut seed) % 9 + 1) as i32;
        let b = (next_random(&mut seed) % 99 + 1) as i32;
        cases.push((s, a, b));
    }
    let mut check: i64 = 0;
    let mut zeros = 0;
    for (s, a, b) in &cases {
        let got = find_lex_smallest_string(s, *a, *b);
        for c in got.chars() {
            if c == '0' {
                zeros += 1;
            }
            check = (check * 31 + (c as i64 - '0' as i64) + 1) % 1000000007;
        }
    }
    println!("200 cases of 100 digits: {zeros} zeros in the answers, checksum {check}");
}
