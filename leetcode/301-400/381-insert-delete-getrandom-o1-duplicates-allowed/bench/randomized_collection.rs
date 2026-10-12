// Benchmark mirror of randomized_collection.kara (#381): a Vec of
// elements, a HashMap from each value to its positions, and each
// position's index in its value's list.
use std::collections::HashMap;

struct RandomizedCollection {
    vals: Vec<i64>,
    slot: Vec<i64>,
    positions: HashMap<i64, Vec<i64>>,
    seed: i64,
}

impl RandomizedCollection {
    fn new() -> Self {
        RandomizedCollection { vals: Vec::new(), slot: Vec::new(), positions: HashMap::new(), seed: 381 }
    }

    fn insert(&mut self, val: i64) -> bool {
        let p = self.vals.len() as i64;
        self.vals.push(val);
        let list = self.positions.entry(val).or_insert_with(Vec::new);
        self.slot.push(list.len() as i64);
        list.push(p);
        list.len() == 1
    }

    fn remove(&mut self, val: i64) -> bool {
        let p = match self.positions.get_mut(&val) {
            None => return false,
            Some(list) => {
                let p = list.pop().unwrap();
                if list.is_empty() {
                    self.positions.remove(&val);
                }
                p
            }
        };
        let last = self.vals.len() as i64 - 1;
        if p < last {
            let moved = self.vals[last as usize];
            let k = self.slot[last as usize];
            self.vals[p as usize] = moved;
            self.slot[p as usize] = k;
            self.positions.get_mut(&moved).unwrap()[k as usize] = p;
        }
        self.vals.pop();
        self.slot.pop();
        true
    }

    fn get_random(&mut self) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        self.vals[((self.seed / 65536) % self.vals.len() as i64) as usize]
    }

    fn len(&self) -> i64 {
        self.vals.len() as i64
    }
}

fn main() {
    let mut rc = RandomizedCollection::new();
    let mut seed: i64 = 381;
    let mut checksum: i64 = 0;
    for _ in 0..20000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let op = (seed / 65536) % 3;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let x = (seed / 64) % 100000;
        let v = if op == 0 {
            if rc.insert(x) { 1 } else { 0 }
        } else if op == 1 {
            if rc.remove(x) { 1 } else { 0 }
        } else if rc.len() > 0 {
            rc.get_random() + 2
        } else {
            7
        };
        checksum = (checksum * 31 + v) % 1000000007;
    }
    println!("checksum {} size {}", checksum, rc.len());
}
