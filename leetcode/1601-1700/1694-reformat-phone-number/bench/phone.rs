// LeetCode #1694: Reformat Phone Number -- the bench's Rust mirror: the ★
// arm on 100000 random numbers of 100 characters, all drawn first, each
// answered 40 times.

fn reformat_number(number: &str) -> String {
    let digits: String = number.chars().filter(|c| c.is_ascii_digit()).collect();
    let mut blocks: Vec<&str> = Vec::new();
    let mut at = 0;
    while digits.len() - at > 4 {
        blocks.push(&digits[at..at + 3]);
        at += 3;
    }
    if digits.len() - at == 4 {
        blocks.push(&digits[at..at + 2]);
        blocks.push(&digits[at + 2..]);
    } else {
        blocks.push(&digits[at..]);
    }
    blocks.join("-")
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 40;
    let length = 100;
    let alphabet = b"0123456789 -";
    let mut seed = 1694;
    let mut numbers: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut number = String::new();
        for i in 0..length {
            let pick = if i < 2 { next_random(&mut seed) % 10 } else { next_random(&mut seed) % 12 };
            number.push(alphabet[pick as usize] as char);
        }
        numbers.push(number);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for number in numbers.iter() {
            let answer = reformat_number(number);
            let bytes = answer.as_bytes();
            let len = bytes.len() as i64;
            total += len;
            check = (check * 31 + len + bytes[bytes.len() / 2] as i64 + bytes[bytes.len() - 1] as i64 + r) % 1000000007;
        }
    }
    println!("{count} numbers of {length} characters, {rounds} rounds: {total} characters out, checksum {check}");
}
