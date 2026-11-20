// LeetCode #1281 bench, in Rust: the ★ arm (the digits by remainders) on
// every n from 1 to 10^5, 2000 rounds, every answer folded into a checksum.

fn subtract_product_and_sum(n: i64) -> i64 {
    let mut product = 1i64;
    let mut sum = 0i64;
    let mut rest = n;
    while rest > 0 {
        let digit = rest % 10;
        product *= digit;
        sum += digit;
        rest /= 10;
    }
    product - sum
}

fn main() {
    let mut check = 0i64;
    for round in 0..2000 {
        for n in 1..100001 {
            check = (check * 131 + subtract_product_and_sum(n) + round + 1000) % 1000000007;
        }
    }
    println!("2000 rounds of 1 to 100000: checksum {}", check);
}
