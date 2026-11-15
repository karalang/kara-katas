// LeetCode #2169: Count Operations to Obtain Zero -- the benchmark's Rust
// mirror of operations.kara.

fn count_operations(num1: i64, num2: i64) -> i64 {
    let mut a = num1.max(num2);
    let mut b = num1.min(num2);
    let mut ops = 0;
    while b > 0 {
        ops += a / b;
        let rest = a % b;
        a = b;
        b = rest;
    }
    ops
}

fn main() {
    let mut total = 0i64;
    let mut check = 0i64;
    for a in 0..=3000i64 {
        for b in 0..=3000i64 {
            let ops = count_operations(a, b);
            total += ops;
            check = (check * 31 + ops) % 1000000007;
        }
    }
    println!("9006001 solves: {} in all, checksum {}", total, check);
}
