// LeetCode #2229: Check if an Array Is Consecutive -- the benchmark's
// Rust mirror of consecutive.kara: the span against the count, and a
// `HashSet` to find a repeat.

use std::collections::HashSet;

fn is_consecutive(nums: &[i64]) -> bool {
    let mut seen: HashSet<i64> = HashSet::new();
    let mut smallest = nums[0];
    let mut largest = nums[0];
    for &x in nums {
        if seen.contains(&x) {
            return false;
        }
        seen.insert(x);
        smallest = smallest.min(x);
        largest = largest.max(x);
    }
    largest - smallest + 1 == nums.len() as i64
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
    let mut seed = 2229;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for l in 0..4 {
        let mut nums: Vec<i64> = (0..100000).collect();
        for i in (1..100000usize).rev() {
            let j = (wide_random(&mut seed) % (i as i64 + 1)) as usize;
            nums.swap(i, j);
        }
        if l >= 2 {
            let from = (wide_random(&mut seed) % 100000) as usize;
            let to = (wide_random(&mut seed) % 100000) as usize;
            nums[to] = nums[from];
        }
        lists.push(nums);
    }
    let mut yes = 0;
    let mut check: i64 = 0;
    for _ in 0..25 {
        for l in 0..4 {
            // punch: two numbers trade places before each answer
            let i = (wide_random(&mut seed) % 100000) as usize;
            let j = (wide_random(&mut seed) % 100000) as usize;
            lists[l].swap(i, j);
            let answer = is_consecutive(&lists[l]);
            if answer {
                yes += 1;
            }
            check = (check * 31 + lists[l][i] + if answer { 1 } else { 2 }) % 1000000007;
        }
    }
    println!("100 answers: {yes} consecutive, checksum {check}");
}
