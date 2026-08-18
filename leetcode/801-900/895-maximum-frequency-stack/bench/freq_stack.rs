// Bench mirror for LeetCode #895 — same algorithm as the Kara version.
use std::collections::HashMap;

struct FreqStack {
    freq: HashMap<i64, i64>,
    buckets: HashMap<i64, Vec<i64>>,
    maxfreq: i64,
}

impl FreqStack {
    fn new() -> Self {
        FreqStack { freq: HashMap::new(), buckets: HashMap::new(), maxfreq: 0 }
    }

    fn push(&mut self, x: i64) {
        let f = *self.freq.get(&x).unwrap_or(&0) + 1;
        self.freq.insert(x, f);
        if f > self.maxfreq {
            self.maxfreq = f;
        }
        let mut b = self.buckets.remove(&f).unwrap_or_default();
        b.push(x);
        self.buckets.insert(f, b);
    }

    fn pop(&mut self) -> i64 {
        let top = self.maxfreq;
        let mut b = self.buckets.remove(&top).unwrap_or_default();
        let x = b[b.len() - 1];
        b.pop();
        let drained = b.is_empty();
        self.buckets.insert(top, b);
        let c = *self.freq.get(&x).unwrap_or(&0) - 1;
        self.freq.insert(x, c);
        if drained {
            self.maxfreq = top - 1;
        }
        x
    }
}

fn run(rounds: i64, steps: i64) -> i64 {
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let mut st = FreqStack::new();
        let mut seed: i64 = 12345 + r;
        let mut live: i64 = 0;
        for i in 0..steps {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            if i % 3 == 2 && live > 0 {
                checksum += st.pop() * (i % 7 + 1);
                live -= 1;
            } else {
                st.push(seed % 12);
                live += 1;
            }
        }
        while live > 0 {
            checksum += st.pop();
            live -= 1;
        }
    }
    checksum
}

fn main() {
    println!("{}", run(120, 3000));
}
