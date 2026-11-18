// LeetCode #2287: Rearrange Characters to Make Target String -- the
// bench, the ★ arm's Rust twin. Two arrays of 26 counts and the least
// quotient.

fn rearrange_characters(s: &str, target: &str) -> i64 {
    let mut have = [0i64; 26];
    let mut need = [0i64; 26];
    for b in s.bytes() {
        have[(b - b'a') as usize] += 1;
    }
    for b in target.bytes() {
        need[(b - b'a') as usize] += 1;
    }
    let mut copies = s.len() as i64;
    for i in 0..26 {
        if need[i] > 0 {
            copies = copies.min(have[i] / need[i]);
        }
    }
    copies
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(len: i64, letters: i64, seed: &mut i64) -> String {
    let mut w = String::new();
    for _ in 0..len {
        w.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    w
}

fn main() {
    let mut seed: i64 = 2287;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..10000 {
        let letters = next_random(&mut seed) % 6 + 1;
        let s_len = next_random(&mut seed) % 100 + 1;
        let t_len = next_random(&mut seed) % 10 + 1;
        let s = word(s_len, letters, &mut seed);
        let target = word(t_len, letters, &mut seed);
        pairs.push((s, target));
    }
    let mut check: i64 = 0;
    for _ in 0..200 {
        let mut total: i64 = 0;
        for (s, target) in pairs.iter() {
            total += rearrange_characters(s, target);
        }
        check = (check * 31 + total) % 1000000007;
    }
    println!("200 passes over 10^4 pairs: checksum {}", check);
}
