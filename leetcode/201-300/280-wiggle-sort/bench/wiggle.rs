// LeetCode 280 bench mirror — Rust. Same greedy, refresh and sink.
const N: usize = 2000000;
const ROUNDS: usize = 30;
fn wiggle_sort(a: &mut [i64]) {
    for i in 1..a.len() {
        if i % 2 == 1 { if a[i] < a[i-1] { a.swap(i, i-1); } }
        else          { if a[i] > a[i-1] { a.swap(i, i-1); } }
    }
}
fn main() {
    let mut src = vec![0i64; N];
    let mut seed: i64 = 20260818;
    for i in 0..N { seed = (seed*1103515245+12345)%2147483648; src[i] = seed % 1000003; }
    let mut work = vec![0i64; N];
    let mut sink = 0i64;
    for _ in 0..ROUNDS {
        work.copy_from_slice(&src);
        wiggle_sort(&mut work);
        let mut h = 0i64;
        for j in 0..N { h = (h*31 + work[j]) % 1000000007; }
        sink = (sink + h) % 1000000007;
    }
    println!("{}", sink);
}
