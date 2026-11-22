// LeetCode #2813: Maximum Elegance of a K-Length Subsequence -- the bench
// in Rust: the ★ arm over 10 cases of 10^5 items, profits up to 10^9 and
// categories up to 30000, k from 1 to 10^5, all drawn first, then each
// answered 5 times.
use std::collections::HashSet;

fn find_maximum_elegance(items: &[Vec<i64>], k: usize) -> i64 {
    let mut order = items.to_vec();
    order.sort_by(|a, b| b[0].cmp(&a[0]));
    let mut seen: HashSet<i64> = HashSet::new();
    let mut repeats: Vec<i64> = Vec::new();
    let mut total = 0i64;
    for item in &order[0..k] {
        total += item[0];
        if !seen.insert(item[1]) {
            repeats.push(item[0]);
        }
    }
    let mut best = total + (seen.len() * seen.len()) as i64;
    for item in &order[k..] {
        if repeats.is_empty() {
            break;
        }
        if seen.insert(item[1]) {
            total += item[0] - repeats.pop().unwrap();
            best = best.max(total + (seen.len() * seen.len()) as i64);
        }
    }
    best
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
    let count = 10;
    let rounds = 5;
    let n = 100000i64;
    let mut rng = Rng(2813);
    let mut cases = Vec::new();
    for _ in 0..count {
        let mut items: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let profit = rng.wide() % 1000000000 + 1;
            let category = rng.wide() % 30000 + 1;
            items.push(vec![profit, category]);
        }
        let k = (rng.wide() % n + 1) as usize;
        cases.push((items, k));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (items, k) in &cases {
            let a = find_maximum_elegance(items, *k);
            total += a;
            check = (check * 31 + a % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} cases of {n}, {rounds} rounds: elegance sums to {total}, checksum {check}");
}
