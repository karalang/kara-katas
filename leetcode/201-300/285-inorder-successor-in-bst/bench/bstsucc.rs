// LeetCode 285 bench mirror — Rust. Same arena, descent and Option-folding sink.
const N: usize = 300000;
const QUERIES: usize = 2000000;
struct Bst { key: Vec<i64>, left: Vec<i64>, right: Vec<i64> }
impl Bst {
    fn insert(&mut self, k: i64) {
        if self.key.is_empty() { self.key.push(k); self.left.push(-1); self.right.push(-1); return; }
        let mut cur = 0usize;
        loop {
            if k < self.key[cur] {
                if self.left[cur] < 0 {
                    self.key.push(k); self.left.push(-1); self.right.push(-1);
                    self.left[cur] = self.key.len() as i64 - 1; return;
                }
                cur = self.left[cur] as usize;
            } else {
                if self.right[cur] < 0 {
                    self.key.push(k); self.left.push(-1); self.right.push(-1);
                    self.right[cur] = self.key.len() as i64 - 1; return;
                }
                cur = self.right[cur] as usize;
            }
        }
    }
    fn successor(&self, target: i64) -> Option<i64> {
        if self.key.is_empty() { return None; }
        let mut cur: i64 = 0;
        let mut best: Option<i64> = None;
        while cur >= 0 {
            let c = cur as usize;
            if self.key[c] > target { best = Some(self.key[c]); cur = self.left[c]; }
            else { cur = self.right[c]; }
        }
        best
    }
}
fn main() {
    let mut t = Bst { key: Vec::with_capacity(N), left: Vec::with_capacity(N), right: Vec::with_capacity(N) };
    let mut seed: i64 = 20260825;
    for _ in 0..N { seed = (seed*1103515245+12345)%2147483648; t.insert(seed % 1000000); }
    let (mut sink, mut found) = (0i64, 0i64);
    for _ in 0..QUERIES {
        seed = (seed*1103515245+12345)%2147483648;
        let s = t.successor(seed % 1000000);
        if s.is_some() { found += 1; }
        sink = (sink*31 + s.unwrap_or(-1)) % 1000000007;
    }
    println!("{} {}", sink, found);
}
