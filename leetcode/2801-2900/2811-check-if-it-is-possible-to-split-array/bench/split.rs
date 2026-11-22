// LeetCode #2811: Check if it is Possible to Split Array -- the bench in
// Rust: the ★ arm over 100000 arrays of 100 numbers up to 100, m from 150
// to 200, all drawn first, then each answered 10 times.

fn can_split_array(nums: &[i64], m: i64) -> bool {
    nums.len() <= 2 || nums.windows(2).any(|w| w[0] + w[1] >= m)
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 100000;
    let rounds = 10;
    let mut rng = Rng(2811);
    let mut cases = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..100).map(|_| rng.next_random() % 100 + 1).collect();
        let m = 150 + rng.next_random() % 51;
        cases.push((nums, m));
    }
    let mut yes = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (nums, m) in &cases {
            let a = if can_split_array(nums, *m) { 1 } else { 0 };
            yes += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of 100, {rounds} rounds: {yes} can split, checksum {check}");
}
