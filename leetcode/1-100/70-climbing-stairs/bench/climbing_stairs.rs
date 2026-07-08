// Benchmark workload — Climbing Stairs (LeetCode #70).
// Rust mirror of bench/climbing_stairs.kara. The ★'s two-counter Fibonacci
// recurrence run K=30_000_000 times over a sweep of n = 1 + k%45, folding each
// result into a rolling polynomial hash. No allocation — a pure integer-add /
// branch benchmark of the recurrence loop. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

fn climb(n: i64) -> i64 {
    if n <= 2 {
        return n;
    }
    let mut a = 1i64;
    let mut b = 2i64;
    let mut i = 3i64;
    while i <= n {
        let next = a + b;
        a = b;
        b = next;
        i += 1;
    }
    b
}

fn main() {
    let total: i64 = 30_000_000;
    let modulus: i64 = 1_000_000_007;
    let span: i64 = 45;

    let mut acc: i64 = 0;
    for k in 0..total {
        let n = 1 + (k % span);
        acc = (acc * 131 + std::hint::black_box(climb(n))) % modulus;
    }
    println!("{}", acc);
}
