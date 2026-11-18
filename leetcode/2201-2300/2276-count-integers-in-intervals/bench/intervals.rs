// LeetCode #2276: Count Integers in Intervals -- the bench, the ★ arm.
use std::collections::BTreeMap;

struct CountIntervals {
    spans: BTreeMap<i64, i64>,
    total: i64,
}

impl CountIntervals {
    fn new() -> Self {
        CountIntervals { spans: BTreeMap::new(), total: 0 }
    }

    fn add(&mut self, left: i64, right: i64) {
        let mut l = left;
        let mut r = right;
        loop {
            let (a, b) = match self.spans.range(..=r).next_back() {
                Some((&a, &b)) => (a, b),
                None => break,
            };
            if b < l {
                break;
            }
            l = l.min(a);
            r = r.max(b);
            self.total -= b - a + 1;
            self.spans.remove(&a);
        }
        self.total += r - l + 1;
        self.spans.insert(l, r);
    }

    fn count(&self) -> i64 {
        self.total
    }
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2276;
    let mut check = 0;
    for t in 0..10 {
        let span = if t % 2 == 0 { 1000000000 } else { 1000000 };
        let mut intervals = CountIntervals::new();
        for _ in 0..100000 {
            if next_random(&mut seed) % 3 == 0 {
                check = (check * 31 + intervals.count()) % 1000000007;
            } else {
                let left = wide_random(&mut seed) % span + 1;
                let right = (left + wide_random(&mut seed) % 1000).min(1000000000);
                intervals.add(left, right);
            }
        }
    }
    println!("10 runs of 10^5: checksum {check}");
}
