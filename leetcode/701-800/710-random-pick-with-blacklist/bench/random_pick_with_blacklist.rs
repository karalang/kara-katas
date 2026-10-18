// LeetCode #710: Random Pick with Blacklist -- the r-th allowed number,
// by binary search.
// Benchmark mirror of the Kara rank arm: sort the blacklist; the r-th
// allowed number is r + i, i the first index with more than r allowed
// numbers below its blacklisted number.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_below(seed: &mut i64, bound: i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 32768 + lo) % bound
}

struct Solution {
    bound: i64,
    black: Vec<i64>,
    seed: i64,
}

impl Solution {
    fn new(n: i64, blacklist: &[i64], seed: i64) -> Solution {
        let mut black = blacklist.to_vec();
        black.sort();
        Solution { bound: n - black.len() as i64, black, seed }
    }

    fn pick_from(&self, r: i64) -> i64 {
        let mut lo = 0usize;
        let mut hi = self.black.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if self.black[mid] - mid as i64 > r {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        r + lo as i64
    }

    fn pick(&mut self) -> i64 {
        let r = random_below(&mut self.seed, self.bound);
        self.pick_from(r)
    }
}

fn main() {
    let n: i64 = 1000000000;
    let mut seed: i64 = 710;
    let mut blacklist: Vec<i64> = Vec::new();
    for i in 0..100000 {
        blacklist.push(i * 10000 + random_below(&mut seed, 10000));
    }
    let mut i = 99999usize;
    while i > 0 {
        let j = random_below(&mut seed, i as i64 + 1) as usize;
        blacklist.swap(i, j);
        i -= 1;
    }
    let mut sum: i64 = 0;
    for round in 0..5 {
        let mut s = Solution::new(n, &blacklist, 1 + round);
        for _ in 0..1000000 {
            sum += s.pick();
        }
    }
    println!("5 rounds of 1000000 picks, 100000 of 1000000000 blacklisted: sum {}", sum);
}
