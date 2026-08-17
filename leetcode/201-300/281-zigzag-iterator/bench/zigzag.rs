// LeetCode 281 bench mirror — Rust. Same cursor iterator, same skip scan.
const K: usize = 64;
const ROUNDS: usize = 2200;
fn drain_sink(lists: &[Vec<i64>]) -> i64 {
    let mut cursor = [0usize; K];
    let mut remaining: i64 = lists.iter().map(|v| v.len() as i64).sum();
    let mut turn = 0usize;
    let mut tried = 0usize;
    while tried < K && cursor[turn] >= lists[turn].len() { turn = (turn + 1) % K; tried += 1; }
    let (mut h, mut pos) = (0i64, 1i64);
    while remaining > 0 {
        let t = turn;
        let v = lists[t][cursor[t]];
        cursor[t] += 1; remaining -= 1;
        h = (h * 31 + v * pos) % 1000000007; pos += 1;
        turn = (t + 1) % K;
        let mut scan = 0usize;
        while scan < K && cursor[turn] >= lists[turn].len() { turn = (turn + 1) % K; scan += 1; }
    }
    h
}
fn main() {
    let mut seed: i64 = 20260819;
    let mut lists: Vec<Vec<i64>> = Vec::with_capacity(K);
    for _ in 0..K {
        seed = (seed*1103515245+12345)%2147483648;
        let len = 1 + (seed/7) % 2000;
        let mut v = Vec::with_capacity(len as usize);
        for _ in 0..len { seed = (seed*1103515245+12345)%2147483648; v.push(seed % 100003); }
        lists.push(v);
    }
    let mut sink = 0i64;
    for _ in 0..ROUNDS { sink = (sink + drain_sink(&lists)) % 1000000007; }
    println!("{}", sink);
}
