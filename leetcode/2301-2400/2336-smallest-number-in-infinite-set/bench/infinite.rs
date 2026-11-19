// LeetCode #2336: Smallest Number in Infinite Set -- the bench, the ★ arm
// in Rust: every number from `next` on still in the set, and the numbers
// below it that were added back kept in a `BTreeSet`.
use std::collections::BTreeSet;

struct SmallestInfiniteSet {
    next: i64,
    returned: BTreeSet<i64>,
}

impl SmallestInfiniteSet {
    fn new() -> Self {
        SmallestInfiniteSet { next: 1, returned: BTreeSet::new() }
    }

    fn pop_smallest(&mut self) -> i64 {
        if let Some(least) = self.returned.pop_first() {
            return least;
        }
        self.next += 1;
        self.next - 1
    }

    fn add_back(&mut self, num: i64) {
        if num < self.next {
            self.returned.insert(num);
        }
    }
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let ops: Vec<i64> = (0..200000)
        .map(|i| {
            let r = scrambled(i);
            if r % 3 == 0 { r / 3 % 5000 + 1 } else { 0 }
        })
        .collect();
    let mut check = 0i64;
    for _ in 0..50 {
        let mut set = SmallestInfiniteSet::new();
        for &op in &ops {
            if op == 0 {
                check = (check * 31 + set.pop_smallest()) % 1000000007;
            } else {
                set.add_back(op);
            }
        }
    }
    println!("50 passes over 2*10^5 calls: checksum {}", check);
}
