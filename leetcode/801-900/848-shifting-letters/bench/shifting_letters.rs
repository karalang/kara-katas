// Benchmark for #848: Shifting Letters -- Rust twin of the Kāra ★ arm
// (suffix sums, from the back).

fn shifting_letters(s: &str, shifts: &[i64]) -> String {
    let mut bytes = s.as_bytes().to_vec();
    let mut shift = 0;
    for i in (0..bytes.len()).rev() {
        shift = (shift + shifts[i]) % 26;
        bytes[i] = b'a' + ((bytes[i] - b'a') as i64 + shift) as u8 % 26;
    }
    String::from_utf8(bytes).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds = 2000;
    let n = 100000;
    let mut seed: i64 = 848;
    let mut texts: Vec<String> = Vec::new();
    let mut all_shifts: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        let mut shifts: Vec<i64> = Vec::new();
        for _ in 0..n {
            s.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
            shifts.push(next_random(&mut seed) * 4657 % 1000000001);
        }
        texts.push(s);
        all_shifts.push(shifts);
    }
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let out = shifting_letters(&texts[round % count], &all_shifts[round % count]);
        let b = out.as_bytes();
        checksum = (checksum * 31 + b[0] as i64 + b[n / 2] as i64 * 7 + b[n - 1] as i64 * 13) % 1000000007;
    }
    println!("{} rounds of {} strings: checksum {}", rounds, count, checksum);
}
