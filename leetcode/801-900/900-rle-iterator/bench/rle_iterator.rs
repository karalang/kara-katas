// LeetCode #900: RLE Iterator -- bench program, Rust.
//
// The offset arm (the encoding left as it is) over one encoding of
// 200,000 runs of 1 to 1,000 terms with values up to 10^9, built once. Each
// round moves the encoding into a fresh iterator, asks for 1 to 1,000
// terms at a time until the iterator answers -1, folds the answers into a
// checksum, takes the encoding back and changes one run's count.

struct RLEIterator {
    encoding: Vec<i64>,
    i: usize,
    used: i64,
}

impl RLEIterator {
    fn new(encoding: Vec<i64>) -> Self {
        RLEIterator { encoding, i: 0, used: 0 }
    }

    fn next(&mut self, n: i64) -> i64 {
        let mut need = n;
        while self.i < self.encoding.len() {
            let left = self.encoding[self.i] - self.used;
            if left >= need {
                self.used += need;
                return self.encoding[self.i + 1];
            }
            need -= left;
            self.i += 2;
            self.used = 0;
        }
        -1
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let runs: i64 = 200000;
    let rounds: i64 = 140;
    let mut seed: i64 = 900;
    let mut encoding: Vec<i64> = Vec::new();
    for _ in 0..runs {
        encoding.push(1 + next_random(&mut seed) % 1000);
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        encoding.push((hi * 32768 + lo) % 1000000001);
    }
    let mut check: i64 = 0;
    let mut calls: i64 = 0;
    for round in 0..rounds {
        let mut it = RLEIterator::new(encoding);
        loop {
            let got = it.next(1 + next_random(&mut seed) % 1000);
            calls += 1;
            if got == -1 {
                break;
            }
            check = (check * 31 + got) % 1000000007;
        }
        encoding = it.encoding;
        encoding[(2 * (round * 7919 % runs)) as usize] = 1 + next_random(&mut seed) % 1000;
    }
    println!("{} rounds over {} runs: {} calls, checksum {}", rounds, runs, calls, check);
}
