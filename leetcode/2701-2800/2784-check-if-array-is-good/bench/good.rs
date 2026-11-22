// LeetCode #2784: Check if Array is Good -- the bench in Rust: the ★ arm
// over 50000 arrays of 100 numbers, base[99] shuffled and two in three
// with one number changed to one up to 200, all drawn first, then each
// answered 40 times.

fn is_good(nums: &[i64]) -> bool {
    let n = nums.len() as i64 - 1;
    if n < 1 {
        return false;
    }
    let mut counts = vec![0i64; (n + 1) as usize];
    for &v in nums {
        if v < 1 || v > n {
            return false;
        }
        counts[v as usize] += 1;
    }
    (1..n).all(|v| counts[v as usize] == 1) && counts[n as usize] == 2
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn shuffled_base(n: i64, rng: &mut Rng) -> Vec<i64> {
    let mut nums: Vec<i64> = (1..=n).collect();
    nums.push(n);
    for i in (1..n + 1).rev() {
        let j = rng.next_random() % (i + 1);
        nums.swap(i as usize, j as usize);
    }
    nums
}

fn main() {
    let count = 50000;
    let rounds = 40;
    let mut rng = Rng(2784);
    let mut cases = Vec::with_capacity(count);
    for _ in 0..count {
        let mut nums = shuffled_base(99, &mut rng);
        if rng.next_random() % 3 != 0 {
            let at = rng.next_random() % 100;
            nums[at as usize] = rng.next_random() % 200 + 1;
        }
        cases.push(nums);
    }
    let mut good = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in &cases {
            let g = is_good(nums);
            if g {
                good += 1;
            }
            check = (check * 31 + if g { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{count} arrays of 100, {rounds} rounds: {good} good, checksum {check}");
}
