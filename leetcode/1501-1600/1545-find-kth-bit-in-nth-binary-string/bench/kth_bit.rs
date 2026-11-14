// LeetCode #1545: Find Kth Bit in Nth Binary String -- bench: the ★ arm (the
// definition's recursion) asked for every place of S_20, two passes. Rust
// mirror of kth_bit.kara.

fn find_kth_bit(n: i64, k: i64) -> char {
    if n == 1 {
        return '0';
    }
    let middle = 1i64 << (n - 1);
    if k == middle {
        '1'
    } else if k < middle {
        find_kth_bit(n - 1, k)
    } else if find_kth_bit(n - 1, (1i64 << n) - k) == '0' {
        '1'
    } else {
        '0'
    }
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut check = 0i64;
    let mut ones = 0i64;
    for _ in 0..2 {
        for k in 1..1048576i64 {
            let bit = if find_kth_bit(20, k) == '1' { 1 } else { 0 };
            ones += bit;
            check = mix(check, bit);
        }
    }
    println!("2 passes over every place of S_20: {} ones, checksum {}", ones, check);
}
