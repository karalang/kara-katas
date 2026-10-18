// LeetCode #716: Max Stack -- a stack of running maxima beside it.
// Benchmark mirror of the Kara star arm: each value with the largest
// value at or below it; pop_max pops into a buffer until the max is on
// top, drops it, and pushes the buffer back.

struct MaxStack {
    values: Vec<i64>,
    maxes: Vec<i64>,
}

impl MaxStack {
    fn new() -> MaxStack {
        MaxStack { values: Vec::new(), maxes: Vec::new() }
    }

    fn push(&mut self, x: i64) {
        let mut m = x;
        if !self.maxes.is_empty() && self.maxes[self.maxes.len() - 1] > x {
            m = self.maxes[self.maxes.len() - 1];
        }
        self.values.push(x);
        self.maxes.push(m);
    }

    fn pop(&mut self) -> i64 {
        self.maxes.pop();
        self.values.pop().unwrap()
    }

    fn top(&self) -> i64 {
        self.values[self.values.len() - 1]
    }

    fn peek_max(&self) -> i64 {
        self.maxes[self.maxes.len() - 1]
    }

    fn pop_max(&mut self) -> i64 {
        let m = self.peek_max();
        let mut buffer: Vec<i64> = Vec::new();
        while self.top() != m {
            let x = self.pop();
            buffer.push(x);
        }
        self.pop();
        while let Some(x) = buffer.pop() {
            self.push(x);
        }
        m
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 716;
    let mut lists: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..10 {
        let mut calls: Vec<(i64, i64)> = Vec::new();
        let mut size = 0;
        for _ in 0..100000 {
            if size == 0 || next_random(&mut seed) % 2 == 0 {
                let hi = next_random(&mut seed);
                let lo = next_random(&mut seed);
                calls.push((0, (hi * 32768 + lo) % 1000001));
                size += 1;
            } else {
                let kind = 1 + next_random(&mut seed) % 4;
                calls.push((kind, 0));
                if kind == 1 || kind == 4 {
                    size -= 1;
                }
            }
        }
        lists.push(calls);
    }
    let mut sum: i64 = 0;
    for _ in 0..10 {
        for calls in lists.iter() {
            let mut s = MaxStack::new();
            for &(kind, x) in calls.iter() {
                if kind == 0 {
                    s.push(x);
                } else if kind == 1 {
                    sum += s.pop();
                } else if kind == 2 {
                    sum += s.top();
                } else if kind == 3 {
                    sum += s.peek_max();
                } else {
                    sum += s.pop_max();
                }
            }
        }
    }
    println!("10 rounds of 10 lists of 100000 calls: sum {}", sum);
}
