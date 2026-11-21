// LeetCode #2349: Design a Number Container System -- the bench, the ★ arm
// in Rust: a map from each index to its number, and for each number a
// min-first heap (`BinaryHeap` of `Reverse`) of every index ever given it,
// popped lazily by find.

use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};

struct NumberContainers {
    at: HashMap<i64, i64>,
    heaps: HashMap<i64, BinaryHeap<Reverse<i64>>>,
}

impl NumberContainers {
    fn new() -> Self {
        NumberContainers { at: HashMap::new(), heaps: HashMap::new() }
    }

    fn change(&mut self, index: i64, number: i64) {
        self.at.insert(index, number);
        self.heaps.entry(number).or_default().push(Reverse(index));
    }

    fn find(&mut self, number: i64) -> i64 {
        let Some(heap) = self.heaps.get_mut(&number) else {
            return -1;
        };
        while let Some(&Reverse(top)) = heap.peek() {
            if self.at[&top] == number {
                return top;
            }
            heap.pop();
        }
        -1
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // two changes to every find, over 10^5 indices and 1000 numbers
    let mut seed = 2349i64;
    let mut calls: Vec<(i64, i64, i64)> = Vec::new();
    for _ in 0..200000 {
        if next_random(&mut seed) % 3 < 2 {
            let high = next_random(&mut seed);
            let index = (high * 32768 + next_random(&mut seed)) % 100000 + 1;
            calls.push((0, index, next_random(&mut seed) % 1000 + 1));
        } else {
            calls.push((1, next_random(&mut seed) % 1000 + 1, 0));
        }
    }
    let mut check = 0i64;
    for p in 0..20i64 {
        let mut containers = NumberContainers::new();
        for &(kind, a, b) in &calls {
            if kind == 0 {
                containers.change(a, b);
            } else {
                check = (check * 31 + containers.find(a) + p + 2) % 1000000007;
            }
        }
    }
    println!("20 passes over 2 * 10^5 calls: checksum {}", check);
}
