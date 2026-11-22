// LeetCode #2799: Count Complete Subarrays in an Array -- the bench in
// Rust: the ★ arm over 2000 arrays of 1000 numbers, half from 1 to 2000
// and half from 1 to 20, all drawn first, then each answered 20 times.
use std::collections::{HashMap, HashSet};

fn count_complete_subarrays(nums: &[i64]) -> i64 {
    let d = nums.iter().collect::<HashSet<_>>().len();
    let mut counts: HashMap<i64, i64> = HashMap::new();
    let mut start = 0usize;
    let mut complete = 0i64;
    for &v in nums {
        *counts.entry(v).or_insert(0) += 1;
        while counts.len() == d {
            let first = nums[start];
            let held = counts[&first];
            if held == 1 {
                break;
            }
            counts.insert(first, held - 1);
            start += 1;
        }
        if counts.len() == d {
            complete += start as i64 + 1;
        }
    }
    complete
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
    fn wide(&mut self) -> i64 {
        let a = self.next_random();
        a * 32768 + self.next_random()
    }
}

fn main() {
    let count = 2000;
    let rounds = 20;
    let mut rng = Rng(2799);
    let mut cases = Vec::new();
    for c in 0..count {
        let top = if c % 2 == 0 { 2000 } else { 20 };
        let nums: Vec<i64> = (0..1000).map(|_| rng.wide() % top + 1).collect();
        cases.push(nums);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in &cases {
            let a = count_complete_subarrays(nums);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of 1000, {rounds} rounds: complete sum to {total}, checksum {check}");
}
