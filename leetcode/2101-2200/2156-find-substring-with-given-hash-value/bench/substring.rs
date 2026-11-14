// LeetCode #2156: Find Substring With Given Hash Value -- the benchmark's
// Rust mirror of substring.kara.

fn sub_str_hash(s: &str, power: i64, modulo: i64, k: i64, hash_value: i64) -> String {
    let letters: Vec<i64> = s.bytes().map(|b| (b - b'a' + 1) as i64).collect();
    let n = letters.len() as i64;
    let p = power % modulo;
    let mut top = 1 % modulo;
    for _ in 0..k {
        top = top * p % modulo;
    }
    let mut hash = 0i64;
    let mut start = n - k;
    for i in (0..n).rev() {
        hash = (hash * p + letters[i as usize]) % modulo;
        if i + k < n {
            hash = (hash - letters[(i + k) as usize] * top % modulo + modulo) % modulo;
        }
        if i + k <= n && hash == hash_value {
            start = i;
        }
    }
    s[start as usize..(start + k) as usize].to_string()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn window_hash(s: &str, start: i64, k: i64, power: i64, modulo: i64) -> i64 {
    let letters = s.as_bytes();
    let mut hash = 0i64;
    let mut weight = 1 % modulo;
    for j in 0..k {
        hash = (hash + (letters[(start + j) as usize] - b'a' + 1) as i64 * weight) % modulo;
        weight = weight * power % modulo;
    }
    hash
}

fn main() {
    let mut seed = 2156i64;
    let mut strings: Vec<Vec<u8>> = Vec::new();
    for _ in 0..4 {
        let letters: Vec<u8> = (0..20000).map(|_| b'a' + (next_random(&mut seed) % 26) as u8).collect();
        strings.push(letters);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..50i64 {
        for t in 0..4 {
            let at = (next_random(&mut seed) % 20000) as usize;
            strings[t][at] = b'a' + (next_random(&mut seed) % 26) as u8;
            let s = String::from_utf8(strings[t].clone()).unwrap();
            let k = next_random(&mut seed) % 20000 + 1;
            let power = 1000000000 - next_random(&mut seed);
            let modulo = 1000000000 - next_random(&mut seed);
            let start = next_random(&mut seed) % (20000 - k + 1);
            let hash_value = window_hash(&s, start, k, power, modulo);
            let found = sub_str_hash(&s, power, modulo, k, hash_value);
            let bytes = found.as_bytes();
            let len = found.len() as i64;
            total += len;
            check = (check * 31 + len + bytes[0] as i64 + bytes[found.len() - 1] as i64 + round) % 1000000007;
        }
    }
    println!("200 solves: {} letters in all, checksum {}", total, check);
}
