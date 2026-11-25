// LeetCode #1359 bench -- Rust: the product of i (2i - 1) for i from 1 to
// n, modulo 10^9 + 7.
const MOD: i64 = 1_000_000_007;

fn count_orders(n: i32) -> i32 {
    let mut count: i64 = 1;
    for i in 1..=n as i64 {
        count = count * i % MOD * (2 * i - 1) % MOD;
    }
    count as i32
}

fn main() {
    // 3 * 10^5 questions, each n from 1 to 500 drawn from the checksum so
    // far, every answer folded into it
    let mut check: i64 = 0;
    for r in 0..300000 {
        let n = (1 + check % 500) as i32;
        check = (check * 31 + count_orders(n) as i64 + r) % MOD;
    }
    println!("300000 questions: checksum {}", check);
}
