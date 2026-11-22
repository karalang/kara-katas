// LeetCode #2791: Count Paths That Can Form a Palindrome in a Tree -- the
// bench in Rust: the ★ arm over 20 random trees of 10^5 nodes with
// letters from a to z, all drawn first, then each answered 5 times.
use std::collections::HashMap;

fn count_palindrome_paths(parent: &[i64], s: &str) -> i64 {
    let n = parent.len();
    let letters: Vec<i64> = s.bytes().map(|b| (b - 97) as i64).collect();
    let mut children: Vec<Vec<usize>> = vec![Vec::new(); n];
    for i in 1..n {
        children[parent[i] as usize].push(i);
    }
    let mut mask = vec![0i64; n];
    let mut todo = vec![0usize];
    while let Some(u) = todo.pop() {
        for &c in &children[u] {
            mask[c] = mask[u] ^ (1 << letters[c]);
            todo.push(c);
        }
    }
    let mut seen: HashMap<i64, i64> = HashMap::new();
    let mut paths = 0i64;
    for &m in &mask {
        paths += seen.get(&m).copied().unwrap_or(0);
        for b in 0..26 {
            paths += seen.get(&(m ^ (1 << b))).copied().unwrap_or(0);
        }
        *seen.entry(m).or_insert(0) += 1;
    }
    paths
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
    let rounds = 5;
    let n = 100000;
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut rng = Rng(2791);
    let mut cases = Vec::new();
    for _ in 0..count {
        let mut parent = vec![-1i64];
        for i in 1..n {
            parent.push(rng.wide() % i);
        }
        let s: String = (0..n).map(|_| alphabet[(rng.next_random() % 26) as usize]).collect();
        cases.push((parent, s));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (parent, s) in &cases {
            let a = count_palindrome_paths(parent, s);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} trees of 10^5, {rounds} rounds: paths sum to {total}, checksum {check}");
}
