// LeetCode #2790: Maximum Number of Groups With Increasing Length -- the
// bench in Rust: the ★ arm over 20 arrays of 10^5 limits up to 10^9, all
// drawn first, then each answered 10 times, each answer sorting its own
// copy.

fn max_increasing_groups(usage_limits: &[i64]) -> i64 {
    let mut limits = usage_limits.to_vec();
    limits.sort();
    let mut groups = 0i64;
    let mut places = 0i64;
    for &u in &limits {
        places += u;
        if places >= (groups + 1) * (groups + 2) / 2 {
            groups += 1;
        }
    }
    groups
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
    let rounds = 10;
    let mut rng = Rng(2790);
    let mut cases = Vec::new();
    for c in 0..count {
        let top = if c % 2 == 0 { 1000000000 } else { 100000 };
        let limits: Vec<i64> = (0..100000).map(|_| rng.wide() % top + 1).collect();
        cases.push(limits);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for limits in &cases {
            let a = max_increasing_groups(limits);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of 10^5, {rounds} rounds: groups sum to {total}, checksum {check}");
}
