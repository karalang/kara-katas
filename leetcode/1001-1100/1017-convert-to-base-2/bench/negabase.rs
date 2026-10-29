// LeetCode #1017: Convert to Base -2 -- bench
// Mirrors negabase.kara; see ../README.md § Benchmarks.

fn base_neg2(n: i64) -> String {
    if n == 0 {
        return "0".to_string();
    }
    let mut rest = n;
    let mut digits = String::new();
    while rest != 0 {
        let bit = rest & 1;
        digits.push(if bit == 1 { '1' } else { '0' });
        rest = (rest - bit) / -2;
    }
    digits.chars().rev().collect()
}

fn main() {
    let most: i64 = 3000000;
    let mut digits: i64 = 0;
    let mut check: i64 = 0;
    for n in 0..most + 1 {
        let form = base_neg2(n);
        digits += form.len() as i64;
        for b in form.bytes() {
            check = (check * 3 + if b == b'1' { 2 } else { 1 }) % 1000000007;
        }
        check = (check * 3) % 1000000007;
    }
    println!("n = 0..{}: {} digits, checksum {}", most, digits, check);
}
