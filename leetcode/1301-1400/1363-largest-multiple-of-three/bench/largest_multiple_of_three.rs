// LeetCode #1363 bench -- Rust: the digits counted, the sum's residue put
// right by dropping the smallest one or two digits that do it.

fn largest_multiple_of_three(digits: &[i32]) -> String {
    let mut count = [0i64; 10];
    let mut sum: i64 = 0;
    for &d in digits {
        count[d as usize] += 1;
        sum += d as i64;
    }
    let r = (sum % 3) as usize;
    if r != 0 {
        let mut dropped = false;
        for d in [r, r + 3, r + 6] {
            if count[d] > 0 {
                count[d] -= 1;
                dropped = true;
                break;
            }
        }
        let mut left = if dropped { 0 } else { 2 };
        for d in [3 - r, 6 - r, 9 - r] {
            while left > 0 && count[d] > 0 {
                count[d] -= 1;
                left -= 1;
            }
        }
    }
    let mut out = String::new();
    for d in (0..10).rev() {
        for _ in 0..count[d] {
            out.push((b'0' + d as u8) as char);
        }
    }
    if out.starts_with('0') {
        return "0".to_string();
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 arrays of 10^4 digits, the constraints' most, built once; then
    // 10^4 rounds, each setting one digit of one array, both drawn from
    // the checksum so far, and folding the answer's length and three of
    // its digits into the checksum
    let mut seed = 1363;
    let mut arrays: Vec<Vec<i32>> = (0..20)
        .map(|_| (0..10000).map(|_| (next_random(&mut seed) % 10) as i32).collect())
        .collect();
    let mut check: i64 = 0;
    for r in 0..10000 {
        let k = (check % 20) as usize;
        arrays[k][((check / 20) % 10000) as usize] = ((check / 200000) % 10) as i32;
        let answer = largest_multiple_of_three(&arrays[k]);
        let bytes = answer.as_bytes();
        let n = bytes.len();
        let picks = if n == 0 { 0 } else { bytes[0] as i64 * 7 + bytes[n / 2] as i64 * 11 + bytes[n - 1] as i64 * 13 };
        check = (check * 31 + n as i64 + picks + r) % 1000000007;
    }
    println!("10000 rounds over 20 arrays of 10^4 digits: checksum {}", check);
}
