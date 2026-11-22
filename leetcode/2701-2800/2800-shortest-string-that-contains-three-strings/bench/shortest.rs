// LeetCode #2800: Shortest String That Contains Three Strings -- the
// bench in Rust: the ★ arm over 2000 triples of up to 100 letters from a
// and b, all drawn first, then each answered 200 times.

fn merge(s: &str, t: &str) -> String {
    if s.contains(t) {
        return s.to_string();
    }
    for k in (1..=t.len().min(s.len())).rev() {
        if s.ends_with(&t[0..k]) {
            return format!("{}{}", s, &t[k..]);
        }
    }
    format!("{}{}", s, t)
}

fn minimum_string(a: &str, b: &str, c: &str) -> String {
    let words = [a, b, c];
    let orders = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
    let mut best = String::new();
    for order in orders.iter() {
        let s = merge(&merge(words[order[0]], words[order[1]]), words[order[2]]);
        if best.is_empty() || s.len() < best.len() || (s.len() == best.len() && s < best) {
            best = s;
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
    fn word(&mut self, m: i64) -> String {
        let letters = "ab";
        let mut w = String::new();
        for _ in 0..m {
            let r = (self.next_random() % 2) as usize;
            w.push_str(&letters[r..r + 1]);
        }
        w
    }
}

fn digest(s: &str) -> i64 {
    s.bytes().fold(0, |h, b| (h * 131 + b as i64) % 1000000007)
}

fn main() {
    let count = 2000;
    let rounds = 200;
    let mut rng = Rng(2800);
    let mut cases = Vec::new();
    for _ in 0..count {
        let m = rng.next_random() % 100 + 1;
        let a = rng.word(m);
        let m = rng.next_random() % 100 + 1;
        let b = rng.word(m);
        let m = rng.next_random() % 100 + 1;
        let c = rng.word(m);
        cases.push((a, b, c));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (a, b, c) in &cases {
            let s = minimum_string(a, b, c);
            total += s.len() as i64;
            check = (check * 31 + digest(&s) + r) % 1000000007;
        }
    }
    println!("{count} triples of up to 100, {rounds} rounds: lengths sum to {total}, checksum {check}");
}
