// LeetCode #2295: Replace Elements in an Array -- the bench, the ★ arm in
// Rust. A HashMap from each number to its index finds the one to replace
// at once; the replacement takes over the index.
use std::collections::HashMap;

fn array_change(nums: &[i64], operations: &[(i64, i64)]) -> Vec<i64> {
    let mut out = nums.to_vec();
    let mut at: HashMap<i64, usize> = HashMap::with_capacity(out.len());
    for (i, &x) in out.iter().enumerate() {
        at.insert(x, i);
    }
    for &(from, to) in operations {
        let i = at.remove(&from).unwrap();
        out[i] = to;
        at.insert(to, i);
    }
    out
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
    fn wide(&mut self) -> i64 {
        let hi = self.next();
        (hi * 32768 + self.next()) % 1000000 + 1
    }
}

fn main() {
    let mut rng = Rng(2295);
    let mut cases: Vec<(Vec<i64>, Vec<(i64, i64)>)> = Vec::new();
    for _ in 0..10 {
        let n = 100000usize;
        let mut present = vec![false; 1000001];
        let mut nums: Vec<i64> = Vec::new();
        while nums.len() < n {
            let x = rng.wide();
            if !present[x as usize] {
                present[x as usize] = true;
                nums.push(x);
            }
        }
        let mut now = nums.clone();
        let mut operations: Vec<(i64, i64)> = Vec::new();
        for _ in 0..100000 {
            let i = (rng.next() % n as i64) as usize;
            let mut to = rng.wide();
            while present[to as usize] {
                to = to % 1000000 + 1;
            }
            present[now[i] as usize] = false;
            present[to as usize] = true;
            operations.push((now[i], to));
            now[i] = to;
        }
        cases.push((nums, operations));
    }
    let mut check: i64 = 0;
    for _ in 0..3 {
        for (nums, operations) in &cases {
            for x in array_change(nums, operations) {
                check = (check * 31 + x) % 1000000007;
            }
        }
    }
    println!("3 passes over 10 arrays of 10^5 with 10^5 operations: checksum {}", check);
}
