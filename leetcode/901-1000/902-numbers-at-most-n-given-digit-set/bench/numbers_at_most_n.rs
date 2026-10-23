// LeetCode #902: Numbers At Most N Given Digit Set -- bench program, Rust.
//
// Lengths, then the digits of n from the left, asked about every one of
// the 511 sets of the digits 1 to 9, built once, in turn, each time with a
// random n from 1 to 10^9, and the counts folded into a checksum.

fn at_most_n_given_digit_set(digits: &[String], n: i64) -> i64 {
    let s = n.to_string().into_bytes();
    let k = s.len();
    let d = digits.len() as i64;
    let mut count: i64 = 0;
    let mut power: i64 = 1;
    for _ in 1..k {
        power *= d;
        count += power;
    }
    for i in 0..k {
        let rest = k - i - 1;
        let mut ways: i64 = 1;
        for _ in 0..rest {
            ways *= d;
        }
        let mut smaller: i64 = 0;
        let mut equal = false;
        for digit in digits.iter() {
            let c = digit.as_bytes()[0];
            if c < s[i] {
                smaller += 1;
            } else if c == s[i] {
                equal = true;
            }
        }
        count += smaller * ways;
        if !equal {
            return count;
        }
    }
    count + 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let queries: i64 = 8000000;
    let mut sets: Vec<Vec<String>> = Vec::new();
    for mask in 1..512 {
        let mut digits: Vec<String> = Vec::new();
        for c in 1..10 {
            if (mask >> (c - 1)) & 1 == 1 {
                digits.push(c.to_string());
            }
        }
        sets.push(digits);
    }
    let mut seed: i64 = 902;
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for q in 0..queries {
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        let n = 1 + (hi * 32768 + lo) % 1000000000;
        let got = at_most_n_given_digit_set(&sets[(q % 511) as usize], n);
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    println!("{} queries over the 511 digit sets: counts summing to {}, checksum {}", queries, total, check);
}
