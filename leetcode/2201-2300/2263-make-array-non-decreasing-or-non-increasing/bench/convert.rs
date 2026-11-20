// LeetCode #2263: Make Array Non-decreasing or Non-increasing -- Rust
// mirror of the ★ arm (convert.kara): the slope trick on a max-first
// `BinaryHeap`, forwards and over the reversed array, the smaller cost.
// Output is byte-identical to convert.kara.
use std::collections::BinaryHeap;

fn nondecreasing_cost(nums: &[i64]) -> i64 {
    let mut heap = BinaryHeap::new();
    let mut cost = 0;
    for &x in nums {
        heap.push(x);
        if *heap.peek().unwrap() > x {
            cost += heap.pop().unwrap() - x;
            heap.push(x);
        }
    }
    cost
}

fn convert_array(nums: Vec<i64>) -> i64 {
    let reversed: Vec<i64> = nums.iter().rev().copied().collect();
    nondecreasing_cost(&nums).min(nondecreasing_cost(&reversed))
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2263;
    let mut check = 0;
    for _ in 0..400 {
        let nums: Vec<i64> = (0..1000).map(|_| next_random(&mut seed) % 1001).collect();
        check = (check * 31 + convert_array(nums)) % 1000000007;
    }
    println!("400 arrays of 1000: checksum {check}");
}
