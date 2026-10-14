// LeetCode 632 -- Smallest Range Covering Elements from K Lists, bench
// mirror in Rust.
//
// The ★ arm of smallest_range.kara: one value from each list in a
// smallest-first `BinaryHeap` of (value, list, index) triples, with the
// largest held value tracked beside it. Same 10 inputs, same 30 rounds,
// same output line.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn smallest_range(nums: &[Vec<i64>]) -> Vec<i64> {
    let mut queue: BinaryHeap<Reverse<(i64, usize, usize)>> = BinaryHeap::new();
    let mut high = nums[0][0];
    for list in 0..nums.len() {
        queue.push(Reverse((nums[list][0], list, 0)));
        high = high.max(nums[list][0]);
    }
    let mut best_low = 0;
    let mut best_high = 0;
    let mut found = false;
    loop {
        let Reverse((low, list, at)) = queue.pop().unwrap();
        if !found || high - low < best_high - best_low {
            best_low = low;
            best_high = high;
            found = true;
        }
        if at + 1 == nums[list].len() {
            break;
        }
        let next = nums[list][at + 1];
        high = high.max(next);
        queue.push(Reverse((next, list, at + 1)));
    }
    vec![best_low, best_high]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_lists(count: i64, length: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut nums: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut list: Vec<i64> = Vec::new();
        for _ in 0..length {
            let wide = next_random(seed) * 32768 + next_random(seed);
            list.push(wide % 200001 - 100000);
        }
        list.sort();
        nums.push(list);
    }
    nums
}

fn main() {
    let mut seed: i64 = 632;
    let mut inputs: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        inputs.push(random_lists(3500, 50, &mut seed));
    }
    let rounds = 30;
    let mut total = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let range = smallest_range(&inputs[round % 10]);
        total += range[1] - range[0];
        checksum = (checksum * 31 + range[0] * 101 + range[1] + 100000000) % 1000000007;
    }
    println!("10 inputs of 3500 lists, {} rounds: total width {}, checksum {}", rounds, total, checksum);
}
