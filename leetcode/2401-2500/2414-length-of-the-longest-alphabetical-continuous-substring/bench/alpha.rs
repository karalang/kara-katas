// LeetCode #2414: Length of the Longest Alphabetical Continuous Substring
// -- the bench, the ★ arm in Rust: one scan, the run growing while each
// letter follows the one before, the longest run kept.

fn longest_continuous_substring(s: &str) -> i64 {
    let b = s.as_bytes();
    let mut run = 1i64;
    let mut best = 1i64;
    for i in 1..b.len() {
        if b[i] == b[i - 1] + 1 {
            run += 1;
            best = best.max(run);
        } else {
            run = 1;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2414;
    let mut strings: Vec<String> = Vec::new();
    for i in 0..10i64 {
        let mut bytes: Vec<u8> = Vec::new();
        for j in 0..100000usize {
            if j > 0 && bytes[j - 1] < b'z' && next_random(&mut seed) % (i + 2) != 0 {
                bytes.push(bytes[j - 1] + 1);
            } else {
                bytes.push(b'a' + (next_random(&mut seed) % 26) as u8);
            }
        }
        strings.push(String::from_utf8(bytes).unwrap());
    }
    let mut check = 0i64;
    for p in 0..200 {
        for s in &strings {
            check = (check * 31 + longest_continuous_substring(s) + p) % 1000000007;
        }
    }
    println!("200 passes over 10 strings of 10^5 letters: checksum {}", check);
}
