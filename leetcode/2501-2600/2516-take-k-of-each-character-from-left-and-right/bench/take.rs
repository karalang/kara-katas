// LeetCode #2516: Take K of Each Character From Left and Right -- Rust
// mirror of the benchmark (take.kara): the same strings, passes, order
// and checksum.

fn take_characters(s: &str, k: i64) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len() as i64;
    let mut total = [0i64; 3];
    for &b in bytes {
        total[(b - b'a') as usize] += 1;
    }
    if total[0] < k || total[1] < k || total[2] < k {
        return -1;
    }
    let mut inside = [0i64; 3];
    let mut left = 0usize;
    let mut longest = 0i64;
    for right in 0..bytes.len() {
        let c = (bytes[right] - b'a') as usize;
        inside[c] += 1;
        while total[c] - inside[c] < k {
            inside[(bytes[left] - b'a') as usize] -= 1;
            left += 1;
        }
        longest = longest.max((right - left + 1) as i64);
    }
    n - longest
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2516;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..40 {
        let mut s = String::new();
        for _ in 0..100000 {
            s.push((b'a' + (next_random(&mut seed) % 3) as u8) as char);
        }
        strings.push(s);
    }
    let passes = 7;
    let mut check: i64 = 0;
    for p in 0..passes {
        for s in strings.iter() {
            check = (check * 31 + take_characters(s, check % 30001) + 1 + p) % 1000000007;
        }
    }
    println!("{} passes over 40 strings of 10^5: checksum {}", passes, check);
}
