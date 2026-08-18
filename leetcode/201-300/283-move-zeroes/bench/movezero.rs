// LeetCode 283 bench mirror — Rust. Same cursor, refresh and sink.
const N: usize = 2000000;
const ROUNDS: usize = 60;
fn move_zeroes(a: &mut [i64], stores: &mut i64) {
    let mut write = 0usize;
    for i in 0..a.len() {
        if a[i] != 0 { a[write] = a[i]; *stores += 1; write += 1; }
    }
    while write < a.len() { a[write] = 0; *stores += 1; write += 1; }
}
fn main() {
    let mut seed: i64 = 20260821;
    let mut src = vec![0i64; N];
    for i in 0..N {
        seed = (seed*1103515245+12345)%2147483648;
        src[i] = if seed % 2 == 0 { 0 } else { seed % 100003 };
    }
    let mut work = vec![0i64; N];
    let (mut sink, mut total) = (0i64, 0i64);
    for _ in 0..ROUNDS {
        work.copy_from_slice(&src);
        let mut st = 0i64;
        move_zeroes(&mut work, &mut st);
        total += st;
        let mut h = 0i64;
        for j in 0..N { h = (h*31 + work[j]) % 1000000007; }
        sink = (sink + h) % 1000000007;
    }
    println!("{} {}", sink, total);
}
