// Benchmark for #509: Rust mirror of the ★ arm (two running values); see
// fib.kara.

fn fib(n: i64) -> i64 {
    let mut a: i64 = 0;
    let mut b: i64 = 1;
    for _ in 0..n {
        let next = a + b;
        a = b;
        b = next;
    }
    a
}

fn main() {
    // F(n) for n = 0, 1, ..., 30 over and over, 150,000,000 calls, the
    // results added up modulo 10^9 + 7.
    let calls: i64 = 150000000;
    let mut total: i64 = 0;
    for i in 0..calls {
        total = (total + fib(i % 31)) % 1000000007;
    }
    println!("{} calls: total {}", calls, total);
}
