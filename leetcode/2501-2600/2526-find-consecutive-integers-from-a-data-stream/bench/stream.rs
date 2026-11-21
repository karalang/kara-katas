// LeetCode #2526: Find Consecutive Integers from a Data Stream -- Rust
// mirror of the benchmark (stream.kara): the same numbers and passes, each
// a fresh stream fed every number.

struct DataStream {
    value: i64,
    k: i64,
    run: i64,
}

impl DataStream {
    fn new(value: i64, k: i64) -> DataStream {
        DataStream { value, k, run: 0 }
    }

    fn consec(&mut self, num: i64) -> bool {
        self.run = if num == self.value { self.run + 1 } else { 0 };
        self.run >= self.k
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2526;
    let nums: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 3 + 1).collect();
    let passes = 1250;
    let mut check: i64 = 0;
    for p in 0..passes {
        let mut stream = DataStream::new(check % 3 + 1, check % 8 + 1);
        let mut trues = 0;
        for &num in &nums {
            if stream.consec(num) {
                trues += 1;
            }
        }
        check = (check * 31 + trues + p) % 1000000007;
    }
    println!("{passes} passes over 10^5 numbers: checksum {check}");
}
