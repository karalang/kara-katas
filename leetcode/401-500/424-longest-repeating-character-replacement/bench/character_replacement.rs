// Benchmark for #424: mirror of character_replacement.kara (a window
// that never shrinks).

fn character_replacement(s: &str, k: i64) -> i64 {
    let bytes = s.as_bytes();
    let mut count = [0i64; 26];
    let mut best = 0;
    let mut left = 0;
    for right in 0..bytes.len() {
        let c = (bytes[right] - b'A') as usize;
        count[c] += 1;
        best = best.max(count[c]);
        if (right - left + 1) as i64 - best > k {
            count[(bytes[left] - b'A') as usize] -= 1;
            left += 1;
        }
    }
    (bytes.len() - left) as i64
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls: i64 = std::env::args().nth(1).map_or(3000, |s| s.parse().unwrap());
    let size: i64 = 1000000;
    let mut seed: i64 = 424;
    let mut text = String::new();
    while (text.len() as i64) < size {
        let letter = (b'A' + (step(&mut seed) % 5) as u8) as char;
        let run = 1 + step(&mut seed) % 8;
        for _ in 0..run {
            if (text.len() as i64) < size {
                text.push(letter);
            }
        }
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let length = 10000 + step(&mut seed) * 3 % 90000;
        let start = step(&mut seed) * 30 % (size - length);
        let k = step(&mut seed) % 50;
        let answer = character_replacement(&text[start as usize..(start + length) as usize], k);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{calls} calls: total {total}, checksum {checksum}");
}
