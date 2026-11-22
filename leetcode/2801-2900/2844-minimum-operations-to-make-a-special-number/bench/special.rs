// LeetCode #2844: Minimum Operations to Make a Special Number -- the
// bench, mirrored from special.kara: one pass from the right, ending
// the number at the first 0 or 5 after a 0, or 2 or 7 after a 5.

fn minimum_operations(num: &str) -> i64 {
    let digits = num.as_bytes();
    let n = digits.len() as i64;
    let mut zero = false;
    let mut five = false;
    for i in (0..digits.len()).rev() {
        let d = digits[i];
        if (zero && (d == b'0' || d == b'5')) || (five && (d == b'2' || d == b'7')) {
            return n - i as i64 - 2;
        }
        if d == b'0' {
            zero = true;
        }
        if d == b'5' {
            five = true;
        }
    }
    if zero { n - 1 } else { n }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 300;
    let mut seed = 2844;
    let mut numbers: Vec<String> = Vec::new();
    for _ in 0..count {
        let n = next_random(&mut seed) % 100 + 1;
        let mut digits: Vec<u8> = Vec::new();
        for i in 0..n {
            let low = if i == 0 && n > 1 { 1 } else { 0 };
            digits.push((48 + low + next_random(&mut seed) % (10 - low)) as u8);
        }
        numbers.push(String::from_utf8(digits).unwrap());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for num in numbers.iter() {
            let ops = minimum_operations(num);
            total += ops;
            check = (check * 31 + ops + r) % 1000000007;
        }
    }
    println!("{count} numbers, {rounds} rounds: {total} operations, checksum {check}");
}
