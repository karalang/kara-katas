// LeetCode #1540: Can Convert String in K Moves -- bench: the ★ arm (the
// places counted by shift) over 100 pairs of 1 to 20000 letters, each with
// k from 0 to 40000, built once, every pair asked 50 times. Rust mirror of
// convert.kara.

fn can_convert_string(s: &str, t: &str, k: i64) -> bool {
    if s.len() != t.len() {
        return false;
    }
    let (s, t) = (s.as_bytes(), t.as_bytes());
    let mut count = [0i64; 26];
    for i in 0..s.len() {
        let d = (t[i] as i64 - s[i] as i64 + 26) % 26;
        count[d as usize] += 1;
    }
    for d in 1..26 {
        if count[d] > 0 && d as i64 + 26 * (count[d] - 1) > k {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn word(n: i64, letters: i64, seed: &mut i64) -> String {
    let mut w = String::new();
    for _ in 0..n {
        w.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    w
}

fn main() {
    let mut seed = 1540i64;
    let mut pairs = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 20000 + 1;
        let used = next_random(&mut seed) % 26 + 1;
        let s = word(n, used, &mut seed);
        let t = word(n, used, &mut seed);
        let k = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 40001;
        pairs.push((s, t, k));
    }
    let mut check = 0i64;
    let mut yes = 0;
    for _ in 0..50 {
        for (s, t, k) in &pairs {
            let answer = can_convert_string(s, t, *k);
            if answer {
                yes += 1;
            }
            check = mix(check, if answer { 1 } else { 0 });
        }
    }
    println!("50 passes over 100 pairs of up to 20000 letters: {} true, checksum {}", yes, check);
}
