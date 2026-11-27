// LeetCode #1825: Finding MK Average -- the bench in Rust: the fenwick arm
// over 20 calls on windows of 1000 to 49999 numbers, each call adding the same
// 10^5 numbers of 1 to 10^5, built once, and asking for the average after
// every hundredth; each window and its cut are drawn from the checksum so far.
// The Fenwick trees are the arm every mirror language writes the same way; the
// ★ arm's ordered bags have no counterpart in C, Go or Python's standard
// library.
use std::collections::VecDeque;

const TOP: i64 = 100000;

struct MkAverage {
    m: i64,
    k: i64,
    window: VecDeque<i64>,
    count: Vec<i64>,
    total: Vec<i64>,
}

impl MkAverage {
    fn new(m: i64, k: i64) -> MkAverage {
        MkAverage { m, k, window: VecDeque::new(), count: vec![0; TOP as usize + 1], total: vec![0; TOP as usize + 1] }
    }

    fn change(&mut self, x: i64, by: i64) {
        let mut i = x;
        while i <= TOP {
            self.count[i as usize] += by;
            self.total[i as usize] += by * x;
            i += i & -i;
        }
    }

    // the sum of the t smallest numbers of the window
    fn smallest(&self, t: i64) -> i64 {
        let mut at = 0;
        let mut left = t;
        let mut sum = 0;
        let mut step = 1 << 16;
        while step > 0 {
            if at + step <= TOP && self.count[(at + step) as usize] <= left {
                at += step;
                left -= self.count[at as usize];
                sum += self.total[at as usize];
            }
            step /= 2;
        }
        sum + left * (at + 1)
    }

    fn add_element(&mut self, num: i64) {
        self.window.push_back(num);
        self.change(num, 1);
        if self.window.len() as i64 > self.m {
            let old = self.window.pop_front().unwrap();
            self.change(old, -1);
        }
    }

    fn calculate_mk_average(&self) -> i64 {
        if (self.window.len() as i64) < self.m {
            return -1;
        }
        (self.smallest(self.m - self.k) - self.smallest(self.k)) / (self.m - 2 * self.k)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1825;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let hi = next_random(&mut seed);
        nums.push(1 + (hi * 32768 + next_random(&mut seed)) % 100000);
    }
    let mut check: i64 = 0;
    for call in 0..20 {
        let m = 1000 + (check + call) % 49000;
        let k = 1 + (check * 7 + call) % ((m - 1) / 2);
        let mut avg = MkAverage::new(m, k);
        for i in 0..nums.len() {
            avg.add_element(nums[i]);
            if i % 100 == 99 {
                check = (check * 31 + avg.calculate_mk_average() + 2) % 1000000007;
            }
        }
    }
    println!("20 calls: checksum {}", check);
}
