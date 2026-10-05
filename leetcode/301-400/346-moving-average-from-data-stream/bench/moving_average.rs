// Benchmark workload for LeetCode #346 — Rust mirror of moving_average.kara.
use std::collections::VecDeque;

const LEN: i64 = 10000000;
const WINDOW: i64 = 1000;

struct MovingAverage {
    size: i64,
    window: VecDeque<i64>,
    sum: i64,
}

impl MovingAverage {
    fn new(size: i64) -> MovingAverage {
        MovingAverage { size, window: VecDeque::new(), sum: 0 }
    }

    fn next(&mut self, val: i64) -> f64 {
        self.window.push_back(val);
        self.sum += val;
        if self.window.len() as i64 > self.size {
            self.sum -= self.window.pop_front().unwrap();
        }
        self.sum as f64 / self.window.len() as f64
    }
}

fn main() {
    let mut m = MovingAverage::new(WINDOW);
    let mut seed: i64 = 346;
    let mut sink = 0.0f64;
    for _ in 0..LEN {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        sink += m.next(seed / 16 % 200001 - 100000);
    }
    println!("sink {:.3}", sink);
}
