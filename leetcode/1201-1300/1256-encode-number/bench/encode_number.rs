// LeetCode #1256 bench, in Rust: the ★ arm (`num + 1` in binary with its
// leading 1 taken off, the digits found by halving) on 200000 random
// numbers from 0 to 10^9 drawn once, each encoded 20 times; every
// string's length and middle digit folded into a checksum.

fn encode(num: i64) -> String {
    let mut digits = Vec::new();
    let mut x = num + 1;
    while x > 1 {
        digits.push(if x % 2 == 1 { '1' } else { '0' });
        x /= 2;
    }
    digits.iter().rev().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1256;
    let mut nums = Vec::new();
    for _ in 0..200000 {
        let hi = next_random(&mut seed) * 32768;
        nums.push((hi + next_random(&mut seed)) % 1000000001);
    }
    let mut check: i64 = 0;
    for _ in 0..20 {
        for &num in &nums {
            let s = encode(num);
            let mid = if s.is_empty() { 0 } else if s.as_bytes()[s.len() / 2] == b'1' { 2 } else { 1 };
            check = (check * 131 + s.len() as i64 * 3 + mid) % 1000000007;
        }
    }
    println!("20 rounds of 200000 numbers: checksum {check}");
}
