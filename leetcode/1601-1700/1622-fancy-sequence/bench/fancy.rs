// LeetCode #1622: Fancy Sequence -- the bench in Rust, mirroring
// fancy.kara: every value stored under the inverse of one map
// x -> mul x + add, the inverse a Fermat power per append.

const MOD: i64 = 1000000007;

fn power(base: i64, exp: i64) -> i64 {
    let (mut result, mut b, mut e) = (1, base % MOD, exp);
    while e > 0 {
        if e & 1 == 1 {
            result = result * b % MOD;
        }
        b = b * b % MOD;
        e >>= 1;
    }
    result
}

struct Fancy {
    stored: Vec<i64>,
    mul: i64,
    add: i64,
}

impl Fancy {
    fn new() -> Fancy {
        Fancy { stored: Vec::new(), mul: 1, add: 0 }
    }

    fn append(&mut self, val: i32) {
        let shifted = (val as i64 - self.add + MOD) % MOD;
        self.stored.push(shifted * power(self.mul, MOD - 2) % MOD);
    }

    fn add_all(&mut self, inc: i32) {
        self.add = (self.add + inc as i64) % MOD;
    }

    fn mult_all(&mut self, m: i32) {
        self.mul = self.mul * m as i64 % MOD;
        self.add = self.add * m as i64 % MOD;
    }

    fn get_index(&self, idx: i32) -> i32 {
        match self.stored.get(idx as usize) {
            Some(x) => ((x * self.mul + self.add) % MOD) as i32,
            None => -1,
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1622;
    let mut sequences: Vec<Vec<(i64, i32)>> = Vec::new();
    for _ in 0..50 {
        let mut calls: Vec<(i64, i32)> = Vec::new();
        let mut length: i64 = 0;
        for _ in 0..100000 {
            let arg = next_random(&mut seed) % 100 + 1;
            let r = next_random(&mut seed) % 10;
            if r <= 3 {
                calls.push((0, arg as i32));
                length += 1;
            } else if r <= 5 {
                calls.push((1, arg as i32));
            } else if r <= 7 {
                calls.push((2, arg as i32));
            } else {
                let high = next_random(&mut seed);
                let idx = (high * 32768 + next_random(&mut seed)) % (length + length / 4 + 1);
                calls.push((3, idx as i32));
            }
        }
        sequences.push(calls);
    }
    let mut check: i64 = 0;
    let mut misses = 0;
    for calls in &sequences {
        let mut fancy = Fancy::new();
        for &(kind, arg) in calls {
            match kind {
                0 => fancy.append(arg),
                1 => fancy.add_all(arg),
                2 => fancy.mult_all(arg),
                _ => {
                    let got = fancy.get_index(arg) as i64;
                    if got == -1 {
                        misses += 1;
                    }
                    check = (check * 31 + got + 1) % 1000000007;
                }
            }
        }
    }
    println!("50 sequences of 100000 calls: {misses} reads past the end, checksum {check}");
}
