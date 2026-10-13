// Benchmark for #460: mirror of lfu_cache.kara (the ★ arm, a linked list
// per use count) on the same workload.
use std::collections::HashMap;

struct Node {
    key: i64,
    value: i64,
    count: i64,
    prev: usize,
    next: usize,
}

struct LFUCache {
    capacity: usize,
    nodes: Vec<Node>,
    index: HashMap<i64, usize>,
    sentinels: HashMap<i64, usize>,
    least: i64,
    free: Option<usize>,
}

impl LFUCache {
    fn new(capacity: usize) -> LFUCache {
        LFUCache { capacity, nodes: Vec::new(), index: HashMap::new(), sentinels: HashMap::new(), least: 0, free: None }
    }

    fn unlink(&mut self, i: usize) {
        let (prev, next) = (self.nodes[i].prev, self.nodes[i].next);
        self.nodes[prev].next = next;
        self.nodes[next].prev = prev;
    }

    fn append(&mut self, i: usize, count: i64) {
        if !self.sentinels.contains_key(&count) {
            let s = self.nodes.len();
            self.nodes.push(Node { key: -1, value: 0, count, prev: s, next: s });
            self.sentinels.insert(count, s);
        }
        let s = self.sentinels[&count];
        let last = self.nodes[s].prev;
        self.nodes[i].count = count;
        self.nodes[i].prev = last;
        self.nodes[i].next = s;
        self.nodes[last].next = i;
        self.nodes[s].prev = i;
    }

    fn is_empty(&self, count: i64) -> bool {
        let s = self.sentinels[&count];
        self.nodes[s].next == s
    }

    fn touch(&mut self, i: usize) {
        let count = self.nodes[i].count;
        self.unlink(i);
        if self.least == count && self.is_empty(count) {
            self.least = count + 1;
        }
        self.append(i, count + 1);
    }

    fn get(&mut self, key: i64) -> i64 {
        match self.index.get(&key) {
            None => -1,
            Some(&i) => {
                self.touch(i);
                self.nodes[i].value
            }
        }
    }

    fn put(&mut self, key: i64, value: i64) {
        if self.capacity == 0 {
            return;
        }
        if let Some(&i) = self.index.get(&key) {
            self.nodes[i].value = value;
            self.touch(i);
            return;
        }
        if self.index.len() == self.capacity {
            let s = self.sentinels[&self.least];
            let victim = self.nodes[s].next;
            self.unlink(victim);
            self.index.remove(&self.nodes[victim].key);
            self.free = Some(victim);
        }
        let i = match self.free.take() {
            Some(i) => {
                self.nodes[i].key = key;
                self.nodes[i].value = value;
                i
            }
            None => {
                self.nodes.push(Node { key, value, count: 0, prev: 0, next: 0 });
                self.nodes.len() - 1
            }
        };
        self.index.insert(key, i);
        self.append(i, 1);
        self.least = 1;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let capacity = 4096;
    let calls = 10000000;
    let mut seed: i64 = 460;
    let mut cache = LFUCache::new(capacity);
    let mut hits = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let key = (next_random(&mut seed) % 200) * (next_random(&mut seed) % 200);
        if next_random(&mut seed) % 2 == 0 {
            let value = next_random(&mut seed) % 1000000;
            cache.put(key, value);
        } else {
            let answer = cache.get(key);
            if answer >= 0 {
                hits += 1;
            }
            checksum = (checksum * 31 + answer + 2) % 1000000007;
        }
    }
    println!("{} calls on a cache of {}: {} hits, checksum {}", calls, capacity, hits, checksum);
}
