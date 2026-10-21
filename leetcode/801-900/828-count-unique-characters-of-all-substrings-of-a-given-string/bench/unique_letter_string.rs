// Benchmark for #828: Count Unique Characters of All Substrings of a Given
// String -- the ★ arm (each character's contribution).
//
// Mirrors unique_letter_string.kara: a character at i is unique in
// (i - prev) * (next - i) substrings, prev and next the copies of its
// letter beside it; one pass keeps the last two positions of each letter
// and settles the middle one each time a letter recurs.

fn unique_letter_string(s: &str) -> i64 {
    let b = s.as_bytes();
    let n = b.len() as i64;
    let mut last = vec![-1i64; 26];
    let mut before = vec![-1i64; 26];
    let mut total = 0i64;
    for i in 0..n {
        let c = (b[i as usize] - b'A') as usize;
        if last[c] >= 0 {
            total += (last[c] - before[c]) * (i - last[c]);
        }
        before[c] = last[c];
        last[c] = i;
    }
    for c in 0..26 {
        if last[c] >= 0 {
            total += (last[c] - before[c]) * (n - last[c]);
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 32i64;
    let rounds = 12800i64;
    let n = 100000;
    let mut seed = 828i64;
    let mut strings: Vec<String> = Vec::new();
    for g in 0..count {
        let letters = 1 + g % 26;
        let mut s = String::new();
        for _ in 0..n {
            s.push((b'A' + (next_random(&mut seed) % letters) as u8) as char);
        }
        strings.push(s);
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for round in 0..rounds {
        let r = unique_letter_string(&strings[(round % count) as usize]);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    println!("{} rounds of {} strings: total {}, checksum {}", rounds, count, total, checksum);
}
