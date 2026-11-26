fn max_score(s: &str) -> i32 {
    let digits: Vec<u8> = s.bytes().collect();
    let ones = digits.iter().filter(|&&d| d == b'1').count() as i32;
    let mut lead: i32 = 0;
    let mut best = i32::MIN;
    for &d in digits[..digits.len() - 1].iter() {
        lead += if d == b'0' { 1 } else { -1 };
        best = best.max(lead);
    }
    ones + best
}

fn main() {
    let mut seed: i64 = 1422;
    let mut pool = String::new();
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push(if seed / 65536 % 2 == 0 { '0' } else { '1' });
    }
    let mut check: i64 = 0;
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (seed / 65536 % 999501) as usize;
        check = (check * 131 + max_score(&pool[start..start + 500]) as i64) % 1000000007;
    }
    println!("10^6 windows of 500 digits: checksum {}", check);
}
