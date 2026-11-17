// LeetCode #2241: Design an ATM Machine -- the benchmark's Rust mirror of
// atm.kara: the counts of the five banknotes, smallest first; a
// withdrawal plans as many of each as fit, largest first, and takes the
// plan only when it pays the whole amount.

struct Atm {
    counts: Vec<i64>,
}

impl Atm {
    fn new() -> Atm {
        Atm { counts: vec![0; 5] }
    }

    fn deposit(&mut self, banknotes_count: &[i64]) {
        for i in 0..5 {
            self.counts[i] += banknotes_count[i];
        }
    }

    fn withdraw(&mut self, amount: i64) -> Vec<i64> {
        let values = [20i64, 50, 100, 200, 500];
        let mut plan = vec![0i64; 5];
        let mut left = amount;
        for i in (0..5).rev() {
            plan[i] = (left / values[i]).min(self.counts[i]);
            left -= plan[i] * values[i];
        }
        if left != 0 {
            return vec![-1];
        }
        for i in 0..5 {
            self.counts[i] -= plan[i];
        }
        plan
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2241i64;
    let mut paid = 0i64;
    let mut check = 0i64;
    let mut counts = vec![0i64; 5];
    for _ in 0..200 {
        let mut atm = Atm::new();
        for _ in 0..5000 {
            if next_random(&mut seed) % 2 == 0 {
                for i in 0..5 {
                    counts[i] = wide_random(&mut seed) % 1000000001;
                }
                atm.deposit(&counts);
            } else {
                let amount = (wide_random(&mut seed) % 100000000 + 1) * 10;
                let answer = atm.withdraw(amount);
                if answer[0] >= 0 {
                    paid += 1;
                }
                for n in answer.iter() {
                    check = (check * 31 + n % 1000000007 + 1) % 1000000007;
                }
            }
        }
    }
    println!("200 machines of 5000 calls: {} withdrawals paid, checksum {}", paid, check);
}
