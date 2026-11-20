// LeetCode #1756: Design Most Recently Used Queue -- the bench (mru.kara
// in Rust): a Vec.

struct MruQueue {
    values: Vec<i32>,
}

impl MruQueue {
    fn new(n: i32) -> MruQueue {
        MruQueue { values: (1..n + 1).collect() }
    }

    fn fetch(&mut self, k: i32) -> i32 {
        let value = self.values.remove(k as usize - 1);
        self.values.push(value);
        value
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 10000;
    let n: i64 = 2000;
    let calls = 2000;
    let mut seed: i64 = 1756;
    let fetches: Vec<i32> = (0..calls).map(|_| (next_random(&mut seed) % n + 1) as i32).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..count {
        let mut queue = MruQueue::new(n as i32);
        for &k in fetches.iter() {
            let got = queue.fetch(k) as i64;
            sum += got;
            check = (check * 31 + got + r) % 1000000007;
        }
    }
    println!("{} queues of {} values, {} fetches each: fetched values add to {}, checksum {}", count, n, calls, sum, check);
}
