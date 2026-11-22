// LeetCode #2780: Minimum Index of a Valid Split -- the bench in Rust:
// the ★ arm over 20 arrays of 10^5 numbers up to 10^9, each with a
// dominant number, all drawn first, then each answered 100 times.

fn minimum_index(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut x = 0;
    let mut votes = 0i64;
    for &v in nums {
        if votes == 0 {
            x = v;
        }
        votes += if v == x { 1 } else { -1 };
    }
    let total = nums.iter().filter(|&&v| v == x).count() as i64;
    let mut left = 0;
    for i in 0..n - 1 {
        if nums[i as usize] == x {
            left += 1;
        }
        if 2 * left > i + 1 && 2 * (total - left) > n - i - 1 {
            return i;
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
    fn wide(&mut self) -> i64 {
        let a = self.next_random();
        a * 32768 + self.next_random()
    }
}

fn dominated(n: i64, others: i64, top: i64, rng: &mut Rng) -> Vec<i64> {
    let x = rng.wide() % top + 1;
    let many = n / 2 + 1 + rng.wide() % (n - n / 2);
    let mut nums = vec![x; many as usize];
    while (nums.len() as i64) < n {
        let v = rng.wide() % others + 1;
        if v != x {
            nums.push(v);
        }
    }
    for i in (1..n).rev() {
        let j = rng.wide() % (i + 1);
        nums.swap(i as usize, j as usize);
    }
    nums
}

fn main() {
    let count = 20;
    let rounds = 100;
    let mut rng = Rng(2780);
    let cases: Vec<Vec<i64>> = (0..count)
        .map(|_| dominated(100000, 1000000000, 1000000000, &mut rng))
        .collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in &cases {
            let a = minimum_index(nums);
            total += a;
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    println!("{count} arrays of 10^5, {rounds} rounds: indices sum to {total}, checksum {check}");
}
