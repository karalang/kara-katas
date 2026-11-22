// LeetCode #2801: Count Stepping Numbers in Range -- the bench in Rust:
// the ★ arm over 400 ranges of 100-digit bounds made mostly of steps, all
// drawn first, then each answered 20 times.

const MOD: i64 = 1000000007;

fn walk(digits: &[i64], pos: usize, last: i64, tight: bool, started: bool, memo: &mut Vec<Vec<i64>>) -> i64 {
    if pos == digits.len() {
        return if started { 1 } else { 0 };
    }
    let free = started && !tight;
    if free && memo[pos][last as usize] >= 0 {
        return memo[pos][last as usize];
    }
    let top = if tight { digits[pos] } else { 9 };
    let mut ways = 0;
    for d in 0..=top {
        let next_tight = tight && d == top;
        if !started {
            ways += walk(digits, pos + 1, d, next_tight, d > 0, memo);
        } else if (d - last).abs() == 1 {
            ways += walk(digits, pos + 1, d, next_tight, true, memo);
        }
    }
    ways %= MOD;
    if free {
        memo[pos][last as usize] = ways;
    }
    ways
}

fn count_up_to(s: &str) -> i64 {
    let digits: Vec<i64> = s.bytes().map(|b| b as i64 - 48).collect();
    let mut memo = vec![vec![-1i64; 10]; digits.len()];
    walk(&digits, 0, 0, true, false, &mut memo)
}

fn steps(s: &str) -> bool {
    let b = s.as_bytes();
    (1..b.len()).all(|i| (b[i] as i64 - b[i - 1] as i64).abs() == 1)
}

fn count_stepping_numbers(low: &str, high: &str) -> i64 {
    let own = if steps(low) { 1 } else { 0 };
    ((count_up_to(high) - count_up_to(low) + own) % MOD + MOD) % MOD
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
    fn number(&mut self, m: i64) -> String {
        let mut d = self.next_random() % 9 + 1;
        let mut s = d.to_string();
        for _ in 1..m {
            let r = self.next_random() % 10;
            d = if r < 8 {
                if r % 2 == 0 && d > 0 || d == 9 { d - 1 } else { d + 1 }
            } else {
                r
            };
            s.push((b'0' + d as u8) as char);
        }
        s
    }
}

fn main() {
    let count = 400;
    let rounds = 20;
    let mut rng = Rng(2801);
    let mut cases = Vec::new();
    for _ in 0..count {
        let a = rng.number(100);
        let b = rng.number(100);
        cases.push(if a <= b { (a, b) } else { (b, a) });
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (low, high) in &cases {
            let a = count_stepping_numbers(low, high);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} ranges of 100 digits, {rounds} rounds: counts sum to {total}, checksum {check}");
}
