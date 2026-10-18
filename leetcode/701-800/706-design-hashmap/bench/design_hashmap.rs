// LeetCode #706 bench: the ★ arm in Rust. See the .kara twin for the
// workload.

struct MyHashMap {
    buckets: Vec<Vec<(i64, i64)>>,
}

impl MyHashMap {
    fn new() -> MyHashMap {
        let mut buckets: Vec<Vec<(i64, i64)>> = Vec::new();
        for _ in 0..1009 {
            buckets.push(Vec::new());
        }
        MyHashMap { buckets }
    }

    fn put(&mut self, key: i64, value: i64) {
        let b = (key % 1009) as usize;
        for i in 0..self.buckets[b].len() {
            if self.buckets[b][i].0 == key {
                self.buckets[b][i] = (key, value);
                return;
            }
        }
        self.buckets[b].push((key, value));
    }

    fn get(&self, key: i64) -> i64 {
        for &(k, v) in self.buckets[(key % 1009) as usize].iter() {
            if k == key {
                return v;
            }
        }
        -1
    }

    fn remove(&mut self, key: i64) {
        let b = (key % 1009) as usize;
        for i in 0..self.buckets[b].len() {
            if self.buckets[b][i].0 == key {
                self.buckets[b].swap_remove(i);
                return;
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 706;
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..5 {
        for _ in 0..10 {
            let mut map = MyHashMap::new();
            for _ in 0..300000 {
                let op = next_random(&mut seed) % 3;
                let key = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50000;
                if op == 0 {
                    let value = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000;
                    map.put(key, value);
                } else if op == 1 {
                    let value = map.get(key);
                    if value >= 0 {
                        found += 1;
                    }
                    checksum = (checksum * 31 + value + 1) % 1000000007;
                } else {
                    map.remove(key);
                }
            }
        }
    }
    println!("5 rounds of 10 maps of 300000 calls: {found} found, checksum {checksum}");
}
