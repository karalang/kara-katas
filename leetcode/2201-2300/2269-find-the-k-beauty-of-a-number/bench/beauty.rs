// LeetCode #2269: Find the K-Beauty of a Number -- the bench, the ★ arm.

fn divisor_substrings(num: i64, k: usize) -> i64 {
    let s = num.to_string();
    let mut beauty = 0;
    for i in 0..=s.len() - k {
        let part: i64 = s[i..i + k].parse().unwrap();
        if part != 0 && num % part == 0 {
            beauty += 1;
        }
    }
    beauty
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2269;
    let mut check = 0;
    for t in 0..200000 {
        let hi = next_random(&mut seed);
        let num = (hi * 32768 + next_random(&mut seed)) % 1000000000 + 1;
        let k = (t % 9 + 1).min(num.to_string().len());
        check = (check * 31 + divisor_substrings(num, k)) % 1000000007;
    }
    println!("200000 numbers: checksum {check}");
}
