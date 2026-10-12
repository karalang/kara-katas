// Benchmark for #384: mirror of shuffle.kara (Fisher-Yates from the end).

struct Solution {
    original: Vec<i64>,
    seed: i64,
}

impl Solution {
    fn new(nums: Vec<i64>) -> Solution {
        Solution { original: nums, seed: 384 }
    }

    fn below(&mut self, n: i64) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        (self.seed / 65536) % n
    }

    fn shuffle(&mut self) -> Vec<i64> {
        let mut a = self.original.clone();
        let mut i = a.len() as i64 - 1;
        while i > 0 {
            let j = self.below(i + 1);
            a.swap(i as usize, j as usize);
            i -= 1;
        }
        a
    }
}

fn main() {
    let nums: Vec<i64> = (0..1000).map(|i| i * 7 % 1000).collect();
    let mut s = Solution::new(nums);
    let mut checksum: i64 = 0;
    for _ in 0..250000 {
        let a = s.shuffle();
        let mut sum = 0i64;
        for k in 0..a.len() {
            sum += a[k] * (k as i64 + 1);
        }
        checksum = (checksum * 31 + sum) % 1000000007;
    }
    println!("250000 shuffles of 1000 values, checksum {}", checksum);
}
