// LeetCode #2798: Number of Employees Who Met the Target -- the bench in
// Rust: the ★ arm over 20000 teams of 50 with hours and targets up to
// 10^5, all drawn first, then each answered 500 times.

fn number_of_employees_who_met_target(hours: &[i64], target: i64) -> i64 {
    hours.iter().filter(|&&h| h >= target).count() as i64
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
    let count = 20000;
    let rounds = 500;
    let mut rng = Rng(2798);
    let mut cases = Vec::new();
    for _ in 0..count {
        let hours: Vec<i64> = (0..50).map(|_| rng.wide() % 100001).collect();
        let target = rng.wide() % 100001;
        cases.push((hours, target));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (hours, target) in &cases {
            let a = number_of_employees_who_met_target(hours, *target);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} teams of 50, {rounds} rounds: met sum to {total}, checksum {check}");
}
