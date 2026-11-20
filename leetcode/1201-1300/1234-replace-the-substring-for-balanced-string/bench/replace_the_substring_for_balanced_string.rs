// LeetCode #1234 bench: the ★ arm in Rust, over the same 40 strings of
// 10^5 letters and 20 passes as the Kāra bench.

fn index(c: u8) -> usize {
    match c {
        b'Q' => 0,
        b'W' => 1,
        b'E' => 2,
        _ => 3,
    }
}

fn balanced_string(s: &str) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len() as i64;
    let k = n / 4;
    let mut outside = [0i64; 4];
    for &b in bytes {
        outside[index(b)] += 1;
    }
    if outside.iter().all(|&c| c == k) {
        return 0;
    }
    let mut best = n;
    let mut left = 0usize;
    for right in 0..bytes.len() {
        outside[index(bytes[right])] -= 1;
        while left <= right && outside.iter().all(|&c| c <= k) {
            best = best.min((right - left + 1) as i64);
            outside[index(bytes[left])] += 1;
            left += 1;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1234;
    let mut strings: Vec<String> = Vec::new();
    for t in 0..40 {
        let lean = t % 4;
        let mut s = String::new();
        for _ in 0..100000 {
            let r = next_random(&mut seed) % (4 + lean);
            s.push(if r >= 4 || r == 0 { 'Q' } else if r == 1 { 'W' } else if r == 2 { 'E' } else { 'R' });
        }
        strings.push(s);
    }
    let mut check = 0i64;
    for _ in 0..20 {
        for s in &strings {
            check = (check * 131 + balanced_string(s)) % 1000000007;
        }
    }
    println!("40 strings of 10^5 letters, 20 passes: checksum {}", check);
}
