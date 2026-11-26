// LeetCode #1792: Maximum Average Pass Ratio -- the bench in Rust: the ★
// arm over 200 random lists of 1000 classes built once, 4000 calls. A
// max-heap of (gain, class), the gain ordered by `total_cmp`.
use std::cmp::Ordering;
use std::collections::BinaryHeap;

#[derive(PartialEq)]
struct Entry(f64, i64);

impl Eq for Entry {}

impl PartialOrd for Entry {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Entry {
    fn cmp(&self, other: &Self) -> Ordering {
        self.0.total_cmp(&other.0).then(self.1.cmp(&other.1))
    }
}

fn gain(p: i64, t: i64) -> f64 {
    (p + 1) as f64 / (t + 1) as f64 - p as f64 / t as f64
}

fn max_average_ratio(classes: &[Vec<i32>], extra_students: i32) -> f64 {
    let n = classes.len();
    let mut pass: Vec<i64> = classes.iter().map(|c| c[0] as i64).collect();
    let mut total: Vec<i64> = classes.iter().map(|c| c[1] as i64).collect();
    let mut queue = BinaryHeap::new();
    for i in 0..n {
        queue.push(Entry(gain(pass[i], total[i]), i as i64));
    }
    for _ in 0..extra_students {
        let Entry(_, i) = queue.pop().unwrap();
        let i = i as usize;
        pass[i] += 1;
        total[i] += 1;
        queue.push(Entry(gain(pass[i], total[i]), i as i64));
    }
    let mut sum = 0.0;
    for i in 0..n {
        sum += pass[i] as f64 / total[i] as f64;
    }
    sum / n as f64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1792;
    let mut lists: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..200 {
        let mut classes: Vec<Vec<i32>> = Vec::new();
        for _ in 0..1000 {
            let t = 1 + next_random(&mut seed) % 1000;
            let p = 1 + next_random(&mut seed) % t;
            classes.push(vec![p as i32, t as i32]);
        }
        lists.push(classes);
    }
    let mut check: i64 = 0;
    for call in 0..4000i64 {
        let classes = &lists[((check + call) % 200) as usize];
        let extra = 1 + check % 1000;
        let r = max_average_ratio(classes, extra as i32);
        check = (check * 31 + (r * 100000.0 + 0.5).floor() as i64) % 1000000007;
    }
    println!("4000 calls over 200 lists of 1000 classes: checksum {}", check);
}
