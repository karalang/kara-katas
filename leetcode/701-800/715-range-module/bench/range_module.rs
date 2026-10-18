// LeetCode #715: Range Module -- a sorted list of disjoint ranges.
// Benchmark mirror of the Kara star arm: parallel sorted vectors of
// starts and ends, a binary search on the ends, and inserts and removals
// that shift the rest.

struct RangeModule {
    starts: Vec<i64>,
    ends: Vec<i64>,
}

impl RangeModule {
    fn new() -> RangeModule {
        RangeModule { starts: Vec::new(), ends: Vec::new() }
    }

    fn first_ending_after(&self, x: i64) -> usize {
        let mut lo = 0;
        let mut hi = self.ends.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if self.ends[mid] > x {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        lo
    }

    fn add_range(&mut self, left: i64, right: i64) {
        let i = self.first_ending_after(left - 1);
        let mut lo = left;
        let mut hi = right;
        let mut j = i;
        while j < self.starts.len() && self.starts[j] <= right {
            if self.starts[j] < lo {
                lo = self.starts[j];
            }
            if self.ends[j] > hi {
                hi = self.ends[j];
            }
            j += 1;
        }
        if j == i {
            self.starts.insert(i, lo);
            self.ends.insert(i, hi);
        } else {
            self.starts[i] = lo;
            self.ends[i] = hi;
            for _ in i + 1..j {
                self.starts.remove(i + 1);
                self.ends.remove(i + 1);
            }
        }
    }

    fn query_range(&self, left: i64, right: i64) -> bool {
        let i = self.first_ending_after(left);
        i < self.starts.len() && self.starts[i] <= left && self.ends[i] >= right
    }

    fn remove_range(&mut self, left: i64, right: i64) {
        let mut i = self.first_ending_after(left);
        if i < self.starts.len() && self.starts[i] < left {
            let end = self.ends[i];
            self.ends[i] = left;
            if end > right {
                self.starts.insert(i + 1, right);
                self.ends.insert(i + 1, end);
                return;
            }
            i += 1;
        }
        while i < self.starts.len() && self.starts[i] < right {
            if self.ends[i] > right {
                self.starts[i] = right;
                return;
            }
            self.starts.remove(i);
            self.ends.remove(i);
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_below(seed: &mut i64, bound: i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 32768 + lo) % bound
}

fn main() {
    let mut seed: i64 = 715;
    let mut lists: Vec<Vec<(i64, i64, i64)>> = Vec::new();
    for _ in 0..10 {
        let mut calls: Vec<(i64, i64, i64)> = Vec::new();
        for _ in 0..100000 {
            let kind = next_random(&mut seed) % 3;
            let left = 1 + random_below(&mut seed, 10000000);
            let right = left + 1 + random_below(&mut seed, 10000);
            calls.push((kind, left, right));
        }
        lists.push(calls);
    }
    let mut held: i64 = 0;
    for _ in 0..10 {
        for calls in lists.iter() {
            let mut m = RangeModule::new();
            for &(kind, left, right) in calls.iter() {
                if kind == 0 {
                    m.add_range(left, right);
                } else if kind == 1 {
                    m.remove_range(left, right);
                } else if m.query_range(left, right) {
                    held += 1;
                }
            }
        }
    }
    println!("10 rounds of 10 lists of 100000 calls: {} queries held", held);
}
