// LeetCode #2743: Count Substrings Without Repeating Character -- the
// bench (substrings.kara in Rust): a window with each letter's last
// place.

fn number_of_special_substrings(s: &str) -> i64 {
    let bytes = s.as_bytes();
    let mut last = [-1i64; 26];
    let mut start = 0i64;
    let mut count = 0i64;
    for i in 0..bytes.len() {
        let letter = (bytes[i] - b'a') as usize;
        start = start.max(last[letter] + 1);
        last[letter] = i as i64;
        count += i as i64 - start + 1;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let n = 100000;
    let rounds: i64 = 300;
    let mut seed = 2743;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..count {
        let k = next_random(&mut seed) % 22 + 5;
        let mut bytes: Vec<u8> = Vec::new();
        for _ in 0..n {
            bytes.push(b'a' + (next_random(&mut seed) % k) as u8);
        }
        words.push(String::from_utf8(bytes).unwrap());
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in words.iter() {
            let found = number_of_special_substrings(s);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    println!("{} words of {} letters, {} rounds: counts sum to {}, checksum {}", count, n, rounds, sum, check);
}
