// LeetCode #2233: Maximum Product After K Increments -- the benchmark's
// Rust mirror of product.kara: the smallest raised k times through a
// min-heap (BinaryHeap of Reverse), then the heap emptied into the product.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn maximum_product(nums: &[i64], k: i64) -> i64 {
    let mut queue: BinaryHeap<Reverse<i64>> = BinaryHeap::new();
    for &x in nums {
        queue.push(Reverse(x));
    }
    for _ in 0..k {
        let Reverse(smallest) = queue.pop().unwrap();
        queue.push(Reverse(smallest + 1));
    }
    let mut product = 1i64;
    while let Some(Reverse(x)) = queue.pop() {
        product = product * x % 1000000007;
    }
    product
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2233i64;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..20000 {
        nums.push(wide_random(&mut seed) % 1000001);
    }
    let mut check = 0i64;
    for _ in 0..150 {
        // punch: one number drawn again before each pass
        let at = (next_random(&mut seed) % 20000) as usize;
        nums[at] = wide_random(&mut seed) % 1000001;
        check = (check * 31 + maximum_product(&nums, 50000)) % 1000000007;
    }
    println!("150 passes over 20000 numbers, k = 50000: checksum {}", check);
}
