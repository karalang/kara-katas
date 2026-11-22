// LeetCode #2802: Find The K-th Lucky Number -- the bench in Rust: the ★
// arm over 200000 k up to 10^9, all drawn first, then each answered 10
// times.

fn kth_lucky_number(k: i64) -> String {
    let n = k + 1;
    let mut top = 1;
    while top * 2 <= n {
        top *= 2;
    }
    let mut lucky = String::new();
    let mut bit = top / 2;
    while bit > 0 {
        lucky.push_str(if n & bit == 0 { "4" } else { "7" });
        bit /= 2;
    }
    lucky
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

fn digest(s: &str) -> i64 {
    s.bytes().fold(0, |h, b| (h * 131 + b as i64) % 1000000007)
}

fn main() {
    let count = 200000;
    let rounds = 10;
    let mut rng = Rng(2802);
    let ks: Vec<i64> = (0..count).map(|_| rng.wide() % 1000000000 + 1).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for &k in &ks {
            let s = kth_lucky_number(k);
            total += s.len() as i64;
            check = (check * 31 + digest(&s) + r) % 1000000007;
        }
    }
    println!("{count} k up to 10^9, {rounds} rounds: lengths sum to {total}, checksum {check}");
}
