// LeetCode #2789: Largest Element in an Array after Merge Operations --
// the bench in Rust: the ★ arm over 20 arrays of 10^5 numbers up to
// 10^6, all drawn first, then each answered 100 times.

fn max_array_value(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut held = nums[n - 1];
    for i in (0..n - 1).rev() {
        held = if nums[i] <= held { held + nums[i] } else { nums[i] };
    }
    held
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
    let count = 20;
    let rounds = 100;
    let mut rng = Rng(2789);
    let mut cases = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..100000).map(|_| rng.wide() % 1000000 + 1).collect();
        cases.push(nums);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in &cases {
            let a = max_array_value(nums);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of 10^5, {rounds} rounds: largest sum to {total}, checksum {check}");
}
