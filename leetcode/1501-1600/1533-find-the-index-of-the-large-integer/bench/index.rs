// LeetCode #1533: Find the Index of the Large Integer -- bench: the ★ arm
// (ternary search) over 100 readers of 2 to 100000 values, built once, each
// searched 20000 times. Rust mirror of index.kara: LeetCode's `&self` API,
// the call count in a `Cell`.

use std::cell::Cell;

struct ArrayReader {
    sums: Vec<i64>,
    calls: Cell<i64>,
}

impl ArrayReader {
    fn from(values: &[i64]) -> ArrayReader {
        let mut sums = vec![0i64; values.len() + 1];
        for i in 0..values.len() {
            sums[i + 1] = sums[i] + values[i];
        }
        ArrayReader { sums, calls: Cell::new(0) }
    }

    fn compare_sub(&self, l: i32, r: i32, x: i32, y: i32) -> i32 {
        self.calls.set(self.calls.get() + 1);
        let left = self.sums[r as usize + 1] - self.sums[l as usize];
        let right = self.sums[y as usize + 1] - self.sums[x as usize];
        if left > right {
            1
        } else if left < right {
            -1
        } else {
            0
        }
    }

    fn length(&self) -> i32 {
        (self.sums.len() - 1) as i32
    }
}

fn get_index(reader: &ArrayReader) -> i64 {
    let mut lo: i32 = 0;
    let mut hi = reader.length() - 1;
    while lo < hi {
        let third = (hi - lo + 1) / 3;
        if third == 0 {
            return if reader.compare_sub(lo, lo, hi, hi) > 0 { lo } else { hi } as i64;
        }
        let second = lo + third;
        match reader.compare_sub(lo, second - 1, second, second + third - 1) {
            1 => hi = second - 1,
            -1 => {
                lo = second;
                hi = second + third - 1;
            }
            _ => lo = second + third,
        }
    }
    lo as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1533i64;
    let mut readers = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 99999 + 2;
        let base = next_random(&mut seed) % 99 + 1;
        let large = base + next_random(&mut seed) % (100 - base) + 1;
        let at = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
        let mut values = vec![base; n as usize];
        values[at as usize] = large;
        readers.push(ArrayReader::from(&values));
    }
    let mut check = 0i64;
    for _ in 0..20000 {
        for reader in &readers {
            check = mix(check, get_index(reader));
        }
    }
    let calls: i64 = readers.iter().map(|r| r.calls.get()).sum();
    println!("20000 passes over 100 readers of up to 100000 values: checksum {}, {} calls", check, calls);
}
