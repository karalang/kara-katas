// Benchmark: LeetCode #981 Time Based Key-Value Store -- the ★ arm, a
// list per key and binary search, on LeetCode's largest sessions of
// 200,000 calls. Mirrors time_map.kara, .c, .py and go-seq/.

use std::collections::HashMap;

struct TimeMap {
    store: HashMap<String, Vec<(i64, String)>>,
}

impl TimeMap {
    fn new() -> Self {
        TimeMap { store: HashMap::new() }
    }

    fn set(&mut self, key: String, value: String, timestamp: i64) {
        self.store.entry(key).or_insert_with(Vec::new).push((timestamp, value));
    }

    fn get(&self, key: &str, timestamp: i64) -> String {
        let Some(list) = self.store.get(key) else {
            return String::new();
        };
        let mut lo = 0;
        let mut hi = list.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if list[mid].0 <= timestamp {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        if lo == 0 {
            String::new()
        } else {
            list[lo - 1].1.clone()
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 20;
    let calls = 200000;
    let keys: Vec<String> = (0..1000i64).map(|i| format!("user{}", i * 7919 % 100000)).collect();
    let values: Vec<String> = (0..100i64).map(|i| format!("value{}", i * 104729 % 1000000)).collect();
    let mut seed = 981;
    let mut found = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut tm = TimeMap::new();
        let mut now = 0;
        for _ in 0..calls {
            let k = (next_random(&mut seed) % 1000) as usize;
            if next_random(&mut seed) % 2 == 0 {
                now += 1 + next_random(&mut seed) % 3;
                let v = (next_random(&mut seed) % 100) as usize;
                tm.set(keys[k].clone(), values[v].clone(), now);
            } else {
                let t = 1 + next_random(&mut seed) % (now + 3);
                let got = tm.get(&keys[k], t);
                if !got.is_empty() {
                    found += 1;
                }
                check = (check * 131 + got.len() as i64) % 1000000007;
                for b in got.bytes() {
                    check = (check * 131 + b as i64) % 1000000007;
                }
            }
        }
    }
    println!("{} rounds of {} calls on 1000 keys: {} values found, checksum {}", rounds, calls, found, check);
}
