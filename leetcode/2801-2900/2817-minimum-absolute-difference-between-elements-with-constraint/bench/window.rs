// LeetCode #2817: Minimum Absolute Difference Between Elements With
// Constraint -- the bench in Rust: the ★ arm over 10 arrays of 10^5
// distinct numbers up to 10^9, shuffled, x from 0 to 10^5 - 1, all drawn
// first, then each answered 3 times. The window is a `BTreeSet`, as
// Kāra's `SortedSet`.
use std::collections::BTreeSet;

fn min_absolute_difference(nums: &[i64], x: usize) -> i64 {
    let mut behind: BTreeSet<i64> = BTreeSet::new();
    let mut best = i64::MAX;
    for i in x..nums.len() {
        behind.insert(nums[i - x]);
        let v = nums[i];
        if let Some(&up) = behind.range(v..).next() {
            best = best.min(up - v);
        }
        if let Some(&down) = behind.range(..=v).next_back() {
            best = best.min(v - down);
        }
        if best == 0 {
            break;
        }
    }
    best
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
    let count = 10;
    let rounds = 3;
    let n = 100000i64;
    let mut rng = Rng(2817);
    let mut cases = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = (0..n).map(|i| i * 10000 + rng.wide() % 10000 + 1).collect();
        for i in (1..n).rev() {
            let j = rng.wide() % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        let x = (rng.wide() % n) as usize;
        cases.push((nums, x));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (nums, x) in &cases {
            let a = min_absolute_difference(nums, *x);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: differences sum to {total}, checksum {check}");
}
