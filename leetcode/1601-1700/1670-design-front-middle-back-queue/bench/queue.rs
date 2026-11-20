// LeetCode #1670: Design Front Middle Back Queue -- the bench's Rust mirror:
// the ★ arm on one run of 1000000 calls, a push three times in five,
// values up to 10^9, drawn first and then replayed 60 times, each on a new
// queue.

use std::collections::VecDeque;

struct FrontMiddleBackQueue {
    front: VecDeque<i32>,
    back: VecDeque<i32>,
}

impl FrontMiddleBackQueue {
    fn new() -> Self {
        FrontMiddleBackQueue { front: VecDeque::new(), back: VecDeque::new() }
    }

    fn balance(&mut self) {
        if self.front.len() > self.back.len() {
            let v = self.front.pop_back().unwrap();
            self.back.push_front(v);
        } else if self.back.len() > self.front.len() + 1 {
            let v = self.back.pop_front().unwrap();
            self.front.push_back(v);
        }
    }

    fn push_front(&mut self, val: i32) {
        self.front.push_front(val);
        self.balance();
    }

    fn push_middle(&mut self, val: i32) {
        self.front.push_back(val);
        self.balance();
    }

    fn push_back(&mut self, val: i32) {
        self.back.push_back(val);
        self.balance();
    }

    fn pop_front(&mut self) -> i32 {
        let val = match self.front.pop_front() {
            Some(v) => v,
            None => match self.back.pop_front() {
                Some(v) => v,
                None => return -1,
            },
        };
        self.balance();
        val
    }

    fn pop_middle(&mut self) -> i32 {
        let taken = if self.front.len() == self.back.len() { self.front.pop_back() } else { self.back.pop_front() };
        let Some(val) = taken else {
            return -1;
        };
        self.balance();
        val
    }

    fn pop_back(&mut self) -> i32 {
        let Some(val) = self.back.pop_back() else {
            return -1;
        };
        self.balance();
        val
    }
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 60;
    let calls = 1000000;
    let mut seed: i64 = 1670;
    let mut run: Vec<(i64, i32)> = Vec::new();
    for _ in 0..calls {
        let r = next_random(&mut seed) % 10;
        let op = if r < 6 { r / 2 } else { r - 3 };
        let val = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000 + 1) as i32;
        run.push((op, val));
    }
    let mut empty: i64 = 0;
    let mut left: usize = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut queue = FrontMiddleBackQueue::new();
        for &(op, val) in &run {
            let got = match op {
                0 => {
                    queue.push_front(val);
                    continue;
                }
                1 => {
                    queue.push_middle(val);
                    continue;
                }
                2 => {
                    queue.push_back(val);
                    continue;
                }
                3 => queue.pop_front(),
                4 => queue.pop_middle(),
                _ => queue.pop_back(),
            };
            if got == -1 {
                empty += 1;
            }
            check = (check * 31 + got as i64 + 1) % 1000000007;
        }
        left += queue.front.len() + queue.back.len();
    }
    println!("{} calls, {} rounds: {} pops on an empty queue, {} values left, checksum {}", calls, rounds, empty, left, check);
}
