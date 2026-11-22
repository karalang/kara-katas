// LeetCode #2710: Remove Trailing Zeros From a String -- the bench
// (zeros.kara in Rust): an index walks back over the zeros, and the
// digits before it are copied out.

fn remove_trailing_zeros(num: &str) -> String {
    let digits = num.as_bytes();
    let mut end = digits.len();
    while digits[end - 1] == b'0' {
        end -= 1;
    }
    num[..end].to_string()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20000;
    let rounds = 20;
    let mut seed: i64 = 2710;
    let mut numbers: Vec<String> = Vec::new();
    for _ in 0..count {
        let zeros = next_random(&mut seed) % 1000;
        let mut num = String::new();
        num.push((b'1' + (next_random(&mut seed) % 9) as u8) as char);
        for _ in 1..1000 - zeros {
            num.push((b'0' + (next_random(&mut seed) % 10) as u8) as char);
        }
        for _ in 0..zeros {
            num.push('0');
        }
        numbers.push(num);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for num in numbers.iter() {
            let out = remove_trailing_zeros(num);
            let kept = out.len() as i64;
            sum += kept;
            check = (check * 31 + kept + out.as_bytes()[out.len() - 1] as i64 + r) % 1000000007;
        }
    }
    println!("{} numbers of 1000 digits, {} rounds: {} digits kept, checksum {}", count, rounds, sum, check);
}
