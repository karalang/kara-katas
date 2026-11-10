// LeetCode #2080: Range Frequency Queries -- Rust mirror of the ★ arm's
// benchmark (frequency.kara): 10 arrays of 10^5 values, each built into a
// `HashMap` of every value's places once and then asked 1000000 queries.

use std::collections::HashMap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

struct RangeFreqQuery {
    places: HashMap<i64, Vec<i64>>,
}

impl RangeFreqQuery {
    fn new(arr: &[i64]) -> Self {
        let mut places: HashMap<i64, Vec<i64>> = HashMap::new();
        for (i, &v) in arr.iter().enumerate() {
            places.entry(v).or_default().push(i as i64);
        }
        RangeFreqQuery { places }
    }

    fn query(&self, left: i64, right: i64, value: i64) -> i64 {
        match self.places.get(&value) {
            Some(at) => (at.partition_point(|&p| p <= right) - at.partition_point(|&p| p < left)) as i64,
            None => 0,
        }
    }
}

fn main() {
    let mut seed = 2080;
    let n = 100000i64;
    let (mut total, mut check) = (0i64, 0i64);
    for t in 0..10 {
        let top = [100, 1000, 10000][t % 3];
        let arr: Vec<i64> = (0..n).map(|_| next_random(&mut seed) % top + 1).collect();
        let index = RangeFreqQuery::new(&arr);
        for _ in 0..1000000 {
            let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let b = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let value = if next_random(&mut seed) % 2 == 0 {
                arr[((next_random(&mut seed) * 32768 + next_random(&mut seed)) % n) as usize]
            } else {
                next_random(&mut seed) % (top + 1) + 1
            };
            let c = index.query(a.min(b), a.max(b), value);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("10000000 queries: sum {}, checksum {}", total, check);
}
