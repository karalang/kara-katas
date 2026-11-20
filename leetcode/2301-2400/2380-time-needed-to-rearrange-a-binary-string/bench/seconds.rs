// LeetCode #2380: Time Needed to Rearrange a Binary String -- the bench,
// the ★ arm in Rust: one pass, each 1 after some 0 taking the larger of
// one more second than the 1 before it and the 0s before it.

fn seconds_to_remove_occurrences(s: &str) -> i64 {
    let mut zeros = 0i64;
    let mut seconds = 0i64;
    for &c in s.as_bytes() {
        if c == b'0' {
            zeros += 1;
        } else if zeros > 0 {
            seconds = (seconds + 1).max(zeros);
        }
    }
    seconds
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 100 strings of 1000 digits, string s 1 with a chance of 1 + s % 10
    // in 12; pass p asks for string (s + 7 p) % 100 in turn
    let mut seed = 2380i64;
    let mut strings: Vec<String> = Vec::new();
    for s in 0..100i64 {
        let digits: Vec<u8> = (0..1000).map(|_| if next_random(&mut seed) % 12 < 1 + s % 10 { b'1' } else { b'0' }).collect();
        strings.push(String::from_utf8(digits).unwrap());
    }
    let mut check = 0i64;
    for p in 0..500i64 {
        for s in 0..100i64 {
            check = (check * 31 + seconds_to_remove_occurrences(&strings[((s + 7 * p) % 100) as usize]) + p) % 1000000007;
        }
    }
    println!("500 passes over 100 strings of 1000 digits: checksum {}", check);
}
