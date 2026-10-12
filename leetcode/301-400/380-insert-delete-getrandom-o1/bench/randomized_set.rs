// Benchmark for #380: mirror of randomized_set.kara (the open-addressing
// arm).

struct RandomizedSet {
    vals: Vec<i64>,
    slots: Vec<Option<(i64, i64)>>,
    seed: i64,
}

impl RandomizedSet {
    fn new() -> RandomizedSet {
        RandomizedSet { vals: Vec::new(), slots: vec![None; 8], seed: 380 }
    }

    fn home(&self, val: i64) -> usize {
        let h = val.wrapping_mul(-7046029254386353131);
        ((h >> 32) & (self.slots.len() as i64 - 1)) as usize
    }

    fn find(&self, val: i64) -> usize {
        let mask = self.slots.len() - 1;
        let mut i = self.home(val);
        loop {
            match self.slots[i] {
                None => return i,
                Some((v, _)) => {
                    if v == val {
                        return i;
                    }
                }
            }
            i = (i + 1) & mask;
        }
    }

    fn set_position(&mut self, val: i64, pos: i64) {
        let i = self.find(val);
        self.slots[i] = Some((val, pos));
    }

    fn grow(&mut self) {
        let old = std::mem::replace(&mut self.slots, Vec::new());
        self.slots = vec![None; 2 * old.len()];
        for slot in old.iter() {
            if let Some((v, p)) = *slot {
                self.set_position(v, p);
            }
        }
    }

    fn insert(&mut self, val: i64) -> bool {
        if self.slots[self.find(val)].is_some() {
            return false;
        }
        if 2 * (self.vals.len() + 1) > self.slots.len() {
            self.grow();
        }
        let pos = self.vals.len() as i64;
        self.set_position(val, pos);
        self.vals.push(val);
        true
    }

    fn delete_slot(&mut self, i: usize) {
        let mask = self.slots.len() - 1;
        let mut gap = i;
        let mut j = (i + 1) & mask;
        self.slots[gap] = None;
        loop {
            match self.slots[j] {
                None => return,
                Some((v, p)) => {
                    let h = self.home(v);
                    let stays = if gap <= j { gap < h && h <= j } else { gap < h || h <= j };
                    if !stays {
                        self.slots[gap] = Some((v, p));
                        self.slots[j] = None;
                        gap = j;
                    }
                }
            }
            j = (j + 1) & mask;
        }
    }

    fn remove(&mut self, val: i64) -> bool {
        let i = self.find(val);
        let pos = match self.slots[i] {
            None => return false,
            Some((_, p)) => p as usize,
        };
        self.delete_slot(i);
        let last = self.vals.pop().unwrap();
        if pos < self.vals.len() {
            self.vals[pos] = last;
            self.set_position(last, pos as i64);
        }
        true
    }

    fn get_random(&mut self) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        self.vals[((self.seed / 65536) % self.vals.len() as i64) as usize]
    }
}

fn main() {
    let mut s = RandomizedSet::new();
    let mut seed: i64 = 380;
    let mut checksum: i64 = 0;
    for _ in 0..20000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let op = (seed / 65536) % 3;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let x = (seed / 64) % 200000;
        let v = if op == 0 {
            if s.insert(x) { 1 } else { 0 }
        } else if op == 1 {
            if s.remove(x) { 1 } else { 0 }
        } else if !s.vals.is_empty() {
            s.get_random()
        } else {
            7
        };
        checksum = (checksum * 31 + v) % 1000000007;
    }
    println!("checksum {} size {}", checksum, s.vals.len());
}
