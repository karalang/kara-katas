// LeetCode #2166: Design Bitset -- the benchmark's Rust mirror of
// bitset.kara.

struct Bitset {
    bits: Vec<bool>,
    flipped: bool,
    ones: i64,
}

impl Bitset {
    fn new(size: i64) -> Bitset {
        Bitset { bits: vec![false; size as usize], flipped: false, ones: 0 }
    }

    fn fix(&mut self, idx: i64) {
        let i = idx as usize;
        if self.bits[i] == self.flipped {
            self.bits[i] = !self.flipped;
            self.ones += 1;
        }
    }

    fn unfix(&mut self, idx: i64) {
        let i = idx as usize;
        if self.bits[i] != self.flipped {
            self.bits[i] = self.flipped;
            self.ones -= 1;
        }
    }

    fn flip(&mut self) {
        self.flipped = !self.flipped;
        self.ones = self.bits.len() as i64 - self.ones;
    }

    fn all(&self) -> bool {
        self.ones == self.bits.len() as i64
    }

    fn one(&self) -> bool {
        self.ones > 0
    }

    fn count(&self) -> i64 {
        self.ones
    }

    fn to_string(&self) -> String {
        let mut text = String::new();
        for &bit in self.bits.iter() {
            text.push(if bit != self.flipped { '1' } else { '0' });
        }
        text
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let size = 100000i64;
    let mut bits = Bitset::new(size);
    let mut seed = 2166i64;
    let mut check = 0i64;
    for i in 0..5000000 {
        if i % 500000 == 499999 {
            for b in bits.to_string().bytes() {
                check = (check * 31 + b as i64) % 1000000007;
            }
            continue;
        }
        let pick = next_random(&mut seed) % 16;
        let answer = if pick < 7 {
            let idx = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % size;
            bits.fix(idx);
            0
        } else if pick < 13 {
            let idx = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % size;
            bits.unfix(idx);
            0
        } else if pick == 13 {
            bits.flip();
            0
        } else if pick == 14 {
            if bits.all() { 2 } else if bits.one() { 1 } else { 0 }
        } else {
            bits.count()
        };
        check = (check * 31 + answer) % 1000000007;
    }
    println!("5000000 calls: checksum {}", check);
}
