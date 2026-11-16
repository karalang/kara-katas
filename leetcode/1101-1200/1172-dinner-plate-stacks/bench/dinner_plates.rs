// LeetCode #1172: Dinner Plate Stacks -- the ★ arm's bench in Rust: the
// stacks in a Vec and a BinaryHeap<Reverse<i64>> of the indices that may
// have room, an index whose stack is full or gone dropped when it comes to
// the top. The same 60 streams of 200000 calls.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

struct DinnerPlates {
    capacity: usize,
    stacks: Vec<Vec<i64>>,
    open: BinaryHeap<Reverse<usize>>,
}

impl DinnerPlates {
    fn new(capacity: usize) -> Self {
        DinnerPlates { capacity, stacks: Vec::new(), open: BinaryHeap::new() }
    }

    fn push(&mut self, val: i64) {
        while let Some(&Reverse(i)) = self.open.peek() {
            if i < self.stacks.len() && self.stacks[i].len() < self.capacity {
                break;
            }
            self.open.pop();
        }
        if self.open.is_empty() {
            self.open.push(Reverse(self.stacks.len()));
            self.stacks.push(Vec::new());
        }
        let Reverse(i) = *self.open.peek().unwrap();
        self.stacks[i].push(val);
        if self.stacks[i].len() == self.capacity {
            self.open.pop();
        }
    }

    fn pop(&mut self) -> i64 {
        if self.stacks.is_empty() {
            return -1;
        }
        self.pop_at_stack(self.stacks.len() - 1)
    }

    fn pop_at_stack(&mut self, index: usize) -> i64 {
        if index >= self.stacks.len() || self.stacks[index].is_empty() {
            return -1;
        }
        let val = self.stacks[index].pop().unwrap();
        self.open.push(Reverse(index));
        while matches!(self.stacks.last(), Some(s) if s.is_empty()) {
            self.stacks.pop();
        }
        val
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let streams = 60;
    let calls = 200000;
    let capacities = [1usize, 7, 100, 20000];
    let mut seed = 1172i64;
    let (mut pops, mut misses, mut check) = (0i64, 0i64, 0i64);
    for s in 0..streams {
        let capacity = capacities[s % 4];
        let spread = (20000 / capacity + 1) as i64;
        let mut d = DinnerPlates::new(capacity);
        for _ in 0..calls {
            let r = next_random(&mut seed) % 10;
            let got = if r < 6 {
                d.push(1 + next_random(&mut seed) % 20000);
                continue;
            } else if r < 8 {
                d.pop()
            } else {
                d.pop_at_stack((next_random(&mut seed) % spread) as usize)
            };
            pops += 1;
            if got == -1 {
                misses += 1;
            }
            check = (check * 131 + got + 2) % 1000000007;
        }
    }
    println!("{streams} streams of {calls} calls: {pops} pops, {misses} empty, checksum {check}");
}
