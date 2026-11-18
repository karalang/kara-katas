// LeetCode #2259: Remove Digit From Number to Maximize Result -- Rust
// mirror of the ★ arm: the first occurrence followed by a larger digit,
// else the last occurrence. Same workload and checksum as remove.kara.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn remove_digit(number: &str, digit: char) -> String {
    let bytes = number.as_bytes();
    let d = digit as u8;
    let mut last = 0;
    for i in 0..bytes.len() {
        if bytes[i] == d {
            last = i;
            if i + 1 < bytes.len() && bytes[i + 1] > d {
                break;
            }
        }
    }
    format!("{}{}", &number[..last], &number[last + 1..])
}

fn main() {
    let mut seed = 2259;
    let mut pool = String::new();
    for _ in 0..1000000 {
        pool.push((b'1' + (next_random(&mut seed) % 9) as u8) as char);
    }
    let mut check: i64 = 0;
    for _ in 0..1000000 {
        let hi = next_random(&mut seed);
        let at = ((hi * 32768 + next_random(&mut seed)) % (1000000 - 100)) as usize;
        let number = &pool[at..at + 100];
        let digit = number.as_bytes()[50] as char;
        let answer = remove_digit(number, digit);
        for b in answer.bytes() {
            check = (check * 131 + b as i64) % 1000000007;
        }
    }
    println!("10^6 numbers of 100 digits: checksum {}", check);
}
