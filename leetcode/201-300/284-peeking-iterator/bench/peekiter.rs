// LeetCode 284 bench mirror — Rust. Same eager wrapper and operation mix.
const N: usize = 200000;
const ROUNDS: usize = 320;
struct Source { data: Vec<i64>, pos: usize, pulls: i64 }
impl Source {
    fn has_next(&self) -> bool { self.pos < self.data.len() }
    fn next(&mut self) -> i64 { let v = self.data[self.pos]; self.pos += 1; self.pulls += 1; v }
}
struct Peeking { src: Source, slot: i64, full: bool }
fn make_peeking(data: &[i64]) -> Peeking {
    let mut src = Source { data: data.to_vec(), pos: 0, pulls: 0 };
    let (mut slot, mut full) = (0i64, false);
    if src.has_next() { slot = src.next(); full = true; }
    Peeking { src, slot, full }
}
impl Peeking {
    fn peek(&self) -> i64 { self.slot }
    fn has_next(&self) -> bool { self.full }
    fn next(&mut self) -> i64 {
        let v = self.slot;
        if self.src.has_next() { self.slot = self.src.next(); } else { self.full = false; }
        v
    }
}
fn main() {
    let mut seed: i64 = 20260823;
    let mut data = vec![0i64; N];
    for i in 0..N { seed = (seed*1103515245+12345)%2147483648; data[i] = seed % 100003; }
    let (mut sink, mut total) = (0i64, 0i64);
    for _ in 0..ROUNDS {
        let mut p = make_peeking(&data);
        let (mut h, mut pos) = (0i64, 1i64);
        while p.has_next() {
            h = (h*31 + p.peek()*pos) % 1000000007;
            h = (h*31 + p.peek()) % 1000000007;
            let v = p.next();
            h = (h*31 + v) % 1000000007;
            pos += 1;
        }
        total += p.src.pulls;
        sink = (sink + h) % 1000000007;
    }
    println!("{} {}", sink, total);
}
