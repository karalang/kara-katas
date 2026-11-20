// LeetCode #1702: Maximum Binary String After Change -- the bench's Rust
// mirror: the ★ arm on 50 random strings of 100000 digits, all drawn
// first, each answered 40 times.

// one 0 left, at the first 0 plus the zeros less one
fn maximum_binary_string(binary: &str) -> String {
    let digits = binary.as_bytes();
    let mut first: i64 = -1;
    let mut zeros: i64 = 0;
    for (i, &b) in digits.iter().enumerate() {
        if b == b'0' {
            if first < 0 {
                first = i as i64;
            }
            zeros += 1;
        }
    }
    if zeros == 0 {
        return binary.to_string();
    }
    let mut out = String::with_capacity(digits.len());
    for i in 0..digits.len() as i64 {
        out.push(if i == first + zeros - 1 { '0' } else { '1' });
    }
    out
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds = 40;
    let n: usize = 100000;
    let mut seed = 1702;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        // each digit a 1 with a chance of its string's own, 0 to 10 in 10
        let lean = next_random(&mut seed) % 11;
        let mut binary = String::with_capacity(n);
        for _ in 0..n {
            binary.push(if next_random(&mut seed) % 10 < lean { '1' } else { '0' });
        }
        strings.push(binary);
    }
    let mut ones: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for binary in strings.iter() {
            let answer = maximum_binary_string(binary);
            let digits = answer.as_bytes();
            // the 0's place, or the length when none is left
            let zero = digits.iter().position(|&b| b == b'0').unwrap_or(digits.len()) as i64;
            let len = digits.len() as i64;
            ones += len - if zero < len { 1 } else { 0 };
            check = (check * 31 + digits[(check % len) as usize] as i64 + zero) % 1000000007;
        }
    }
    println!("{count} strings of {n} digits, {rounds} rounds: {ones} ones, checksum {check}");
}
