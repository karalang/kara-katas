// LeetCode #2786: Visit Array Positions to Maximize Score -- the bench in
// Rust: the ★ arm over 20 arrays of 10^5 numbers up to 10^6 with x up to
// 10^6, all drawn first, then each answered 100 times.

fn max_score(nums: &[i64], x: i64) -> i64 {
    let unreached = -1000000000000000i64;
    let mut best = [unreached, unreached];
    best[(nums[0] % 2) as usize] = nums[0];
    for &v in &nums[1..] {
        let p = (v % 2) as usize;
        best[p] = best[p].max(best[1 - p] - x) + v;
    }
    best[0].max(best[1])
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
    let mut rng = Rng(2786);
    let mut cases = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..100000).map(|_| rng.wide() % 1000000 + 1).collect();
        let x = rng.wide() % 1000000 + 1;
        cases.push((nums, x));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (nums, x) in &cases {
            let a = max_score(nums, *x);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of 10^5, {rounds} rounds: scores sum to {total}, checksum {check}");
}
