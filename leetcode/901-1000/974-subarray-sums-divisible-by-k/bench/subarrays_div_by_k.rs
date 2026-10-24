// Benchmark: LeetCode #974 Subarray Sums Divisible by K -- the ★ arm,
// counts of prefix remainders, on 20 arrays of 30000 random numbers.
// Mirrors subarrays_div_by_k.kara, .c, .py and go-seq/.

fn subarrays_div_by_k(nums: &[i64], k: i64) -> i64 {
    let mut count = vec![0i64; k as usize];
    count[0] = 1;
    let mut sum = 0;
    let mut total = 0;
    for &x in nums {
        sum += x;
        let r = ((sum % k + k) % k) as usize;
        total += count[r];
        count[r] += 1;
    }
    total
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let rounds = 200;
    let count = 20;
    let mut rng = Rng(974);
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..30000).map(|_| rng.next() % 20001 - 10000).collect();
        let k = 2 + rng.next() % 9999;
        cases.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let c = (r + i) % count;
            let got = subarrays_div_by_k(&cases[c].0, cases[c].1);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} arrays of 30000 numbers: {total} subarrays, checksum {check}");
}
