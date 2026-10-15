// Benchmark for #677: the keys kept sorted, as the Kara sorted arm.

struct MapSum {
    keys: Vec<String>,
    vals: Vec<i64>,
}

fn lower_bound(keys: &[String], word: &str) -> usize {
    let mut lo = 0;
    let mut hi = keys.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        if keys[mid].as_str() < word {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

impl MapSum {
    fn new() -> MapSum {
        MapSum { keys: Vec::new(), vals: Vec::new() }
    }

    fn insert(&mut self, key: String, val: i64) {
        let at = lower_bound(&self.keys, &key);
        if at < self.keys.len() && self.keys[at] == key {
            self.vals[at] = val;
        } else {
            self.keys.insert(at, key);
            self.vals.insert(at, val);
        }
    }

    fn sum(&self, prefix: &str) -> i64 {
        let mut total = 0;
        let mut i = lower_bound(&self.keys, prefix);
        while i < self.keys.len() && self.keys[i].starts_with(prefix) {
            total += self.vals[i];
            i += 1;
        }
        total
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, most: i64) -> String {
    let n = 1 + next_random(seed) % most;
    let mut s = String::new();
    for _ in 0..n {
        s.push((97 + next_random(seed) % 3) as u8 as char);
    }
    s
}

fn main() {
    let rounds = 100;
    let calls = 2000;
    let mut seed: i64 = 677;
    let mut s: i64 = 0;
    for _ in 0..rounds {
        let mut m = MapSum::new();
        for _ in 0..calls {
            let key = random_word(&mut seed, 12);
            let val = 1 + next_random(&mut seed) % 1000;
            m.insert(key, val);
        }
        for _ in 0..calls {
            let prefix = random_word(&mut seed, 3);
            s = (s * 31 + m.sum(&prefix)) % 1000000007;
        }
    }
    println!("{} rounds of {} inserts and {} sums: checksum {}", rounds, calls, calls, s);
}
