// Benchmark for #504 in Rust: the ★ arm (the digits by repeated
// division); see ../convert_to_base7.kara. Each digit is formatted with
// `format!`, as the Kāra arm's `f"{d}"` formats it into a fresh String.

fn convert_to_base7(num: i64) -> String {
    if num == 0 {
        return "0".to_string();
    }
    let mut n = num.abs();
    let mut digits: Vec<i64> = Vec::new();
    while n > 0 {
        digits.push(n % 7);
        n /= 7;
    }
    let mut out = if num < 0 { "-".to_string() } else { String::new() };
    for d in digits.iter().rev() {
        out.push_str(&format!("{d}"));
    }
    out
}

fn main() {
    // 5,000,001 numbers across the whole range, -10^7 to 10^7 in steps
    // of 4. Each string is read back as a decimal number, which the base
    // 7 digits name uniquely, and folded into a checksum.
    let count: i64 = 5000001;
    let mut digits = 0;
    let mut checksum: i64 = 0;
    for i in 0..count {
        let num = -10000000 + 4 * i;
        let s = convert_to_base7(num);
        digits += s.len();
        let read: i64 = s.parse().unwrap();
        checksum = (checksum * 31 + read % 1000000007 + 1000000007) % 1000000007;
    }
    println!("{count} numbers: {digits} characters, checksum {checksum}");
}
