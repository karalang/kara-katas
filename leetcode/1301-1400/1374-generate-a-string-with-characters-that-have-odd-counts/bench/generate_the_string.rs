// LeetCode #1374 bench -- Rust: the ★ arm: n a's when n is odd, and
// n - 1 a's and a b when it is even.

fn generate_the_string(n: i32) -> String {
    if n % 2 == 1 {
        return "a".repeat(n as usize);
    }
    "a".repeat(n as usize - 1) + "b"
}

fn main() {
    // 10^7 rounds, each making the string for an n from 1 to 500, the
    // constraints' range, drawn from the checksum so far, and reading its
    // length and one letter at a place drawn the same way
    let mut check: i64 = 0;
    for r in 0..10000000i64 {
        let n = (1 + check % 500) as i32;
        let s = generate_the_string(n);
        let len = s.len() as i64;
        let b = s.as_bytes()[((check / 500) % len) as usize] as i64;
        check = (check * 31 + len + b + r) % 1000000007;
    }
    println!("10000000 rounds: checksum {check}");
}
