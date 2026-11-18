// LeetCode #1624: Largest Substring Between Two Equal Characters -- the
// bench in Rust, mirroring gap.kara: one pass over the characters, the
// first index of each letter, and at every later sight the gap back to it.

fn max_length_between_equal_characters(s: &str) -> i32 {
    let mut first = [-1i64; 26];
    let mut best: i64 = -1;
    for (i, c) in s.chars().enumerate() {
        let letter = (c as i64 - 'a' as i64) as usize;
        if first[letter] == -1 {
            first[letter] = i as i64;
        } else {
            best = best.max(i as i64 - first[letter] - 1);
        }
    }
    best as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1624;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..100000 {
        let n = next_random(&mut seed) % 300 + 1;
        let mut s = String::new();
        for _ in 0..n {
            s.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for s in &strings {
        let got = max_length_between_equal_characters(s) as i64;
        total += got;
        check = (check * 31 + got + 1) % 1000000007;
    }
    println!("100000 random strings: answers sum to {total}, checksum {check}");
}
