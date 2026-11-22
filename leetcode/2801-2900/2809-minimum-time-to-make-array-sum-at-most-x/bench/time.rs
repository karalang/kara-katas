// LeetCode #2809: Minimum Time to Make Array Sum At Most x -- the bench in
// Rust: the ★ arm over 20 cases of 1000 pairs, nums1 up to 1000 and nums2
// up to 2, x from 3 * 10^5 to 5 * 10^5, all drawn first, then each
// answered 20 times.

fn minimum_time(nums1: &[i64], nums2: &[i64], x: i64) -> i64 {
    let n = nums1.len();
    let mut pairs: Vec<(i64, i64)> = nums2.iter().cloned().zip(nums1.iter().cloned()).collect();
    pairs.sort();
    let mut best = vec![0i64; n + 1];
    for (i, &(b, a)) in pairs.iter().enumerate() {
        for j in (1..=i + 1).rev() {
            best[j] = best[j].max(best[j - 1] + a + j as i64 * b);
        }
    }
    let sum1: i64 = nums1.iter().sum();
    let sum2: i64 = nums2.iter().sum();
    for t in 0..=n {
        if sum1 + t as i64 * sum2 - best[t] <= x {
            return t as i64;
        }
    }
    -1
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 20;
    let rounds = 20;
    let mut rng = Rng(2809);
    let mut cases = Vec::new();
    for _ in 0..count {
        let nums1: Vec<i64> = (0..1000).map(|_| rng.next_random() % 1001).collect();
        let nums2: Vec<i64> = (0..1000).map(|_| rng.next_random() % 3).collect();
        let x = 300000 + (rng.next_random() * 32768 + rng.next_random()) % 200000;
        cases.push((nums1, nums2, x));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (nums1, nums2, x) in &cases {
            let a = minimum_time(nums1, nums2, *x);
            total += a;
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    println!("{count} cases of 1000 pairs, {rounds} rounds: times sum to {total}, checksum {check}");
}
