// Bench mirror of summary_ranges.kara (the sorted-vector arm), same algorithm.

struct SummaryRanges {
    starts: Vec<i64>,
    ends: Vec<i64>,
}

impl SummaryRanges {
    fn new() -> Self {
        SummaryRanges { starts: Vec::new(), ends: Vec::new() }
    }

    fn first_after(&self, value: i64) -> usize {
        let mut lo = 0;
        let mut hi = self.starts.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if self.starts[mid] <= value {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        lo
    }

    fn add_num(&mut self, value: i64) {
        let i = self.first_after(value);
        let joins_left = i > 0 && self.ends[i - 1] >= value - 1;
        if i > 0 && self.ends[i - 1] >= value {
            return;
        }
        let joins_right = i < self.starts.len() && self.starts[i] == value + 1;
        if joins_left && joins_right {
            self.ends[i - 1] = self.ends[i];
            self.starts.remove(i);
            self.ends.remove(i);
        } else if joins_left {
            self.ends[i - 1] = value;
        } else if joins_right {
            self.starts[i] = value;
        } else {
            self.starts.insert(i, value);
            self.ends.insert(i, value);
        }
    }

    fn get_intervals(&self) -> Vec<(i64, i64)> {
        let mut out = Vec::new();
        for i in 0..self.starts.len() {
            out.push((self.starts[i], self.ends[i]));
        }
        out
    }
}

fn next_value(state: &mut i64, limit: i64) -> i64 {
    *state = (*state * 1103515245 + 12345) % 2147483648;
    (*state >> 8) % (limit + 1)
}

fn main() {
    let rounds: i64 = 150;
    let mut sink: i64 = 0;
    for r in 0..rounds {
        let mut stream = SummaryRanges::new();
        let mut state: i64 = 352 + r;
        for i in 1..30001 {
            stream.add_num(next_value(&mut state, 10000));
            if i % 3000 == 0 {
                for (s, e) in stream.get_intervals() {
                    sink = (sink * 31 + s * 7 + e + r) % 1000000007;
                }
            }
        }
    }
    println!("sink {}", sink);
}
