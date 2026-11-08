// LeetCode #1525: Number of Good Ways to Split a String -- bench: the ★
// arm over 200 random strings of 1 to 100000 letters, built once and
// answered 10 times. Each answer takes its own copy of the string, as the
// signature does.

fn num_splits(s: String) -> i64 {
    let b = s.as_bytes();
    let n = b.len();
    let mut left: Vec<i64> = vec![0; n];
    let mut seen = vec![false; 26];
    let mut distinct = 0;
    for i in 0..n {
        let c = (b[i] - 97) as usize;
        if !seen[c] {
            seen[c] = true;
            distinct += 1;
        }
        left[i] = distinct;
    }
    let mut right: Vec<i64> = vec![0; n];
    seen = vec![false; 26];
    distinct = 0;
    for i in (0..n).rev() {
        let c = (b[i] - 97) as usize;
        if !seen[c] {
            seen[c] = true;
            distinct += 1;
        }
        right[i] = distinct;
    }
    let mut good = 0;
    for i in 1..n {
        if left[i - 1] == right[i] {
            good += 1;
        }
    }
    good
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1525i64;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..200 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let letters = next_random(&mut seed) % 26 + 1;
        let mut s = String::new();
        for _ in 0..n {
            s.push((97 + next_random(&mut seed) % letters) as u8 as char);
        }
        strings.push(s);
    }
    let mut check = 0;
    let mut total = 0i64;
    for _ in 0..10 {
        for s in &strings {
            let good = num_splits(s.clone());
            total += good;
            check = mix(check, good);
        }
    }
    println!("10 passes over 200 strings of up to 100000 letters: {} good splits, checksum {}", total, check);
}
