// LeetCode #705 bench: the ★ arm in Rust. See the .kara twin for the
// workload.

struct MyHashSet {
    buckets: Vec<Vec<i64>>,
}

impl MyHashSet {
    fn new() -> MyHashSet {
        let mut buckets: Vec<Vec<i64>> = Vec::new();
        for _ in 0..1009 {
            buckets.push(Vec::new());
        }
        MyHashSet { buckets }
    }

    fn add(&mut self, key: i64) {
        let b = (key % 1009) as usize;
        if !self.buckets[b].contains(&key) {
            self.buckets[b].push(key);
        }
    }

    fn remove(&mut self, key: i64) {
        let b = (key % 1009) as usize;
        let n = self.buckets[b].len();
        for i in 0..n {
            if self.buckets[b][i] == key {
                self.buckets[b].swap_remove(i);
                return;
            }
        }
    }

    fn contains(&self, key: i64) -> bool {
        self.buckets[(key % 1009) as usize].contains(&key)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 705;
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..5 {
        for _ in 0..10 {
            let mut set = MyHashSet::new();
            for _ in 0..300000 {
                let op = next_random(&mut seed) % 3;
                let key = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50000;
                if op == 0 {
                    set.add(key);
                } else if op == 1 {
                    set.remove(key);
                } else {
                    let yes = set.contains(key);
                    if yes {
                        found += 1;
                    }
                    checksum = (checksum * 3 + if yes { 1 } else { 2 }) % 1000000007;
                }
            }
        }
    }
    println!("5 rounds of 10 sets of 300000 calls: {found} found, checksum {checksum}");
}
