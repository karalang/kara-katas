// LeetCode #2043: Simple Bank System -- the ★ arm in Rust, the same
// algorithm and workload as bank.kara: the balances in a Vec indexed by
// account - 1, every call checked whole before anything changes.

struct Bank {
    balance: Vec<i64>,
}

impl Bank {
    fn new(balance: Vec<i64>) -> Bank {
        Bank { balance }
    }

    fn exists(&self, account: i64) -> bool {
        account >= 1 && account <= self.balance.len() as i64
    }

    fn transfer(&mut self, account1: i64, account2: i64, money: i64) -> bool {
        if !self.exists(account1) || !self.exists(account2) || self.balance[(account1 - 1) as usize] < money {
            return false;
        }
        self.balance[(account1 - 1) as usize] -= money;
        self.balance[(account2 - 1) as usize] += money;
        true
    }

    fn deposit(&mut self, account: i64, money: i64) -> bool {
        if !self.exists(account) {
            return false;
        }
        self.balance[(account - 1) as usize] += money;
        true
    }

    fn withdraw(&mut self, account: i64, money: i64) -> bool {
        if !self.exists(account) || self.balance[(account - 1) as usize] < money {
            return false;
        }
        self.balance[(account - 1) as usize] -= money;
        true
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    let mid = next_random(seed);
    (hi * 32768 + mid) * 32768 + next_random(seed)
}

fn problem(n: i64, calls: i64, top: i64, seed: &mut i64) -> (Vec<i64>, Vec<(i64, i64, i64, i64)>) {
    let balance: Vec<i64> = (0..n).map(|_| big_random(seed) % (top + 1)).collect();
    let mut ops = Vec::with_capacity(calls as usize);
    for _ in 0..calls {
        let kind = next_random(seed) % 3;
        let a = big_random(seed) % (n + 2);
        let b = big_random(seed) % (n + 2);
        let money = big_random(seed) % (top + 1);
        ops.push((kind, a, b, money));
    }
    (balance, ops)
}

fn main() {
    let mut seed = 2043i64;
    let (balance, ops) = problem(100000, 1000000, 1000000, &mut seed);
    let mut calls = 0i64;
    let mut succeeded = 0i64;
    let mut check = 0i64;
    for round in 0..40i64 {
        let mut bank = Bank::new(balance.clone());
        for &(kind, a, b, money) in &ops {
            let ok = match kind {
                0 => bank.transfer(a, b, money),
                1 => bank.deposit(a, money),
                _ => bank.withdraw(a, money),
            };
            calls += 1;
            if ok {
                succeeded += 1;
                check = (check * 31 + calls + round) % 1000000007;
            }
        }
    }
    println!("{} calls: {} succeed, checksum {}", calls, succeeded, check);
}
