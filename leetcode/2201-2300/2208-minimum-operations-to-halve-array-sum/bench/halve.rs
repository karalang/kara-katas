// benchmark's Rust mirror of halve.kara (LeetCode #2208, the ★ arm):
// greedily halve the largest number, kept in a `BinaryHeap` of floats
// ordered by `total_cmp` (Kāra's `F64` order), until the halves taken add
// up to half the sum.
use std::cmp::Ordering;
use std::collections::BinaryHeap;

#[derive(PartialEq)]
struct F64(f64);
impl Eq for F64 {}
impl PartialOrd for F64 {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}
impl Ord for F64 {
    fn cmp(&self, other: &Self) -> Ordering {
        self.0.total_cmp(&other.0)
    }
}

fn halve_array(nums: &[i64]) -> i64 {
    let mut heap = BinaryHeap::new();
    let mut total = 0.0;
    for &x in nums {
        total += x as f64;
        heap.push(F64(x as f64));
    }
    let mut removed = 0.0;
    let mut ops = 0;
    while removed < total / 2.0 {
        let top = heap.pop().unwrap().0;
        let half = top / 2.0;
        removed += half;
        heap.push(F64(half));
        ops += 1;
    }
    ops
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2208;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..12 {
        let top = [10, 1000, 10000000][a % 3];
        let mut nums = Vec::new();
        for _ in 0..100000 {
            nums.push(wide_random(&mut seed) % top + 1);
        }
        arrays.push(nums);
    }
    // each array halved once
    let mut check: i64 = 0;
    for nums in &arrays {
        check = (check * 31 + halve_array(nums)) % 1000000007;
    }
    println!("12 arrays of 10^5: checksum {check}");
}
