// LeetCode #1538: Guess the Majority in a Hidden Array -- bench: the ★ arm
// (every bit compared with bit 0, n queries) over 100 readers of 5 to 50000
// bits, built once, each asked 20 times. Rust mirror of majority.kara:
// LeetCode's `&self` API, the call count in a `Cell`.

use std::cell::Cell;

struct ArrayReader {
    nums: Vec<i64>,
    calls: Cell<i64>,
}

impl ArrayReader {
    fn query(&self, a: i32, b: i32, c: i32, d: i32) -> i32 {
        self.calls.set(self.calls.get() + 1);
        let ones = self.nums[a as usize] + self.nums[b as usize] + self.nums[c as usize] + self.nums[d as usize];
        if ones == 0 || ones == 4 {
            4
        } else if ones == 2 {
            0
        } else {
            2
        }
    }

    fn length(&self) -> i32 {
        self.nums.len() as i32
    }
}

fn guess_majority(reader: &ArrayReader) -> i64 {
    let n = reader.length();
    let q0123 = reader.query(0, 1, 2, 3);
    let q1234 = reader.query(1, 2, 3, 4);
    let mut same = vec![true; n as usize];
    same[1] = reader.query(0, 2, 3, 4) == q1234;
    same[2] = reader.query(0, 1, 3, 4) == q1234;
    same[3] = reader.query(0, 1, 2, 4) == q1234;
    same[4] = q1234 == q0123;
    for i in 5..n {
        same[i as usize] = reader.query(1, 2, 3, i) == q0123;
    }
    let mut with_zero = 0i64;
    let mut other = -1i64;
    for i in 0..n as usize {
        if same[i] {
            with_zero += 1;
        } else {
            other = i as i64;
        }
    }
    let n = n as i64;
    if with_zero * 2 > n {
        0
    } else if with_zero * 2 < n {
        other
    } else {
        -1
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1538i64;
    let mut readers = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 49996 + 5;
        let chance = next_random(&mut seed) % 101;
        let mut nums = Vec::new();
        for _ in 0..n {
            nums.push(if next_random(&mut seed) % 100 < chance { 1 } else { 0 });
        }
        readers.push(ArrayReader { nums, calls: Cell::new(0) });
    }
    let mut check = 0i64;
    for _ in 0..20 {
        for reader in &readers {
            check = mix(check, guess_majority(reader));
        }
    }
    let calls: i64 = readers.iter().map(|r| r.calls.get()).sum();
    println!("20 passes over 100 readers of up to 50000 bits: checksum {}, {} calls", check, calls);
}
