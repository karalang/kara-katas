// LeetCode #1073: Adding Two Negabinary Numbers -- the benchmark's Rust
// mirror of negabinary.kara: the same addition from the low end with a
// carry, over 2000 pairs of numbers built once, each added 20 times.

fn add_negabinary(a: &[i64], b: &[i64]) -> Vec<i64> {
    let mut i = a.len() as i64 - 1;
    let mut j = b.len() as i64 - 1;
    let mut carry = 0i64;
    let mut digits: Vec<i64> = Vec::new();
    while i >= 0 || j >= 0 || carry != 0 {
        let mut s = carry;
        if i >= 0 {
            s += a[i as usize];
            i -= 1;
        }
        if j >= 0 {
            s += b[j as usize];
            j -= 1;
        }
        digits.push(s & 1);
        carry = -(s >> 1);
    }
    while digits.len() > 1 && digits[digits.len() - 1] == 0 {
        digits.pop();
    }
    digits.reverse();
    digits
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_number(longest: i64, seed: &mut i64) -> Vec<i64> {
    let n = next_random(seed) % longest + 1;
    if n == 1 {
        return vec![next_random(seed) % 2];
    }
    let mut digits = vec![1];
    for _ in 1..n {
        digits.push(next_random(seed) % 2);
    }
    digits
}

fn main() {
    let mut seed = 1073;
    let mut pairs: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..2000 {
        let a = random_number(1000, &mut seed);
        let b = random_number(1000, &mut seed);
        pairs.push((a, b));
    }
    let mut digits = 0i64;
    let mut check = 0i64;
    for _ in 0..20 {
        for (a, b) in pairs.iter() {
            let x = add_negabinary(a, b);
            digits += x.len() as i64;
            check = (check * 31 + x.len() as i64 + x[x.len() / 2]) % 1000000007;
        }
    }
    println!("40000 calls: {digits} digits, checksum {check}");
}
