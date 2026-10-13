// Benchmark for #480: Rust mirror of the ★ arm (two heaps, deletions put
// off); see sliding_window_median.kara.
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};

struct Window {
    low: BinaryHeap<i64>,
    high: BinaryHeap<Reverse<i64>>,
    gone: HashMap<i64, i64>,
    low_size: i64,
    high_size: i64,
}

impl Window {
    fn new() -> Window {
        Window { low: BinaryHeap::new(), high: BinaryHeap::new(), gone: HashMap::new(), low_size: 0, high_size: 0 }
    }

    fn prune(&mut self) {
        while let Some(&top) = self.low.peek() {
            let left = *self.gone.get(&top).unwrap_or(&0);
            if left == 0 {
                break;
            }
            self.gone.insert(top, left - 1);
            self.low.pop();
        }
        while let Some(&Reverse(top)) = self.high.peek() {
            let left = *self.gone.get(&top).unwrap_or(&0);
            if left == 0 {
                break;
            }
            self.gone.insert(top, left - 1);
            self.high.pop();
        }
    }

    fn balance(&mut self) {
        if self.low_size > self.high_size + 1 {
            let x = self.low.pop().unwrap();
            self.high.push(Reverse(x));
            self.low_size -= 1;
            self.high_size += 1;
        } else if self.low_size < self.high_size {
            let Reverse(x) = self.high.pop().unwrap();
            self.low.push(x);
            self.high_size -= 1;
            self.low_size += 1;
        }
        self.prune();
    }

    fn add(&mut self, x: i64) {
        let goes_low = match self.low.peek() {
            Some(&top) => x <= top,
            None => true,
        };
        if goes_low {
            self.low.push(x);
            self.low_size += 1;
        } else {
            self.high.push(Reverse(x));
            self.high_size += 1;
        }
        self.balance();
    }

    fn remove(&mut self, x: i64) {
        let in_low = x <= *self.low.peek().unwrap();
        *self.gone.entry(x).or_insert(0) += 1;
        if in_low {
            self.low_size -= 1;
        } else {
            self.high_size -= 1;
        }
        self.prune();
        self.balance();
    }

    fn median(&self, k: i64) -> f64 {
        let a = *self.low.peek().unwrap();
        if k % 2 == 1 {
            a as f64
        } else {
            (a + self.high.peek().unwrap().0) as f64 / 2.0
        }
    }
}

fn median_sliding_window(nums: &[i64], k: i64) -> Vec<f64> {
    let mut window = Window::new();
    let mut medians = Vec::new();
    let k_us = k as usize;
    for i in 0..nums.len() {
        window.add(nums[i]);
        if i >= k_us {
            window.remove(nums[i - k_us]);
        }
        if i + 1 >= k_us {
            medians.push(window.median(k));
        }
    }
    medians
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 1000000;
    let mut seed: i64 = 480;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let r = a * 32768 + b;
        nums.push(r * 4 + next_random(&mut seed) % 4 - 2147483648);
    }
    let mut windows: i64 = 0;
    let mut checksum: i64 = 0;
    for k in 1000..1002 {
        for m in median_sliding_window(&nums, k) {
            windows += 1;
            checksum = (checksum * 31 + (m * 2.0) as i64 % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("{} windows: checksum {}", windows, checksum);
}
