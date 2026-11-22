// LeetCode #2806: Account Balance After Rounded Purchase -- the bench in
// Rust: the ★ arm over 10^6 amounts from 0 to 100, all drawn first, then
// each answered 100 times into a running checksum.

fn account_balance_after_purchase(purchase_amount: i64) -> i64 {
    100 - (purchase_amount + 5) / 10 * 10
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 1000000;
    let rounds = 100;
    let mut rng = Rng(2806);
    let amounts: Vec<i64> = (0..count).map(|_| rng.next_random() % 101).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for &p in &amounts {
            let b = account_balance_after_purchase(p);
            total += b;
            check = (check * 31 + b + r) % 1000000007;
        }
    }
    println!("{count} amounts, {rounds} rounds: balances sum to {total}, checksum {check}");
}
