// Benchmark for #409: mirror of longest_palindrome.kara (letter counts).

fn longest_palindrome(s: &str) -> i64 {
    let mut counts = vec![0i64; 128];
    for b in s.bytes() {
        counts[b as usize] += 1;
    }
    let mut length = 0;
    let mut odd = false;
    for i in 0..128 {
        length += counts[i] / 2 * 2;
        if counts[i] % 2 == 1 {
            odd = true;
        }
    }
    if odd { length + 1 } else { length }
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let queries: i64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(300000);
    let size: i64 = 2000000;
    let letters = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let mut seed: i64 = 409;
    let mut text = String::new();
    for _ in 0..size {
        text.push(letters[(step(&mut seed) % 52) as usize] as char);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..queries {
        let len = 1000 + step(&mut seed) % 1001;
        let hi = step(&mut seed);
        let lo = step(&mut seed);
        let start = (hi * 32768 + lo) % (size - len + 1);
        let answer = longest_palindrome(&text[start as usize..(start + len) as usize]);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{} slices of a {}-letter text: total {}, checksum {}", queries, size, total, checksum);
}
