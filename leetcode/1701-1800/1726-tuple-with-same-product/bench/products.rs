// LeetCode #1726: Tuple with Same Product -- the bench (products.kara):
// every pair's product counted in a hash map, each new pair meeting the
// earlier pairs of its product, 8 tuples each.

use std::collections::HashMap;

fn tuple_same_product(nums: &[i32]) -> i32 {
    let mut counts: HashMap<i32, i32> = HashMap::new();
    let mut tuples = 0;
    for i in 0..nums.len() {
        for j in i + 1..nums.len() {
            let seen = counts.entry(nums[i] * nums[j]).or_insert(0);
            tuples += 8 * *seen;
            *seen += 1;
        }
    }
    tuples
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds: i64 = 3;
    let n: usize = 1000;
    let top: usize = 10000;
    let mut seed: i64 = 1726;
    let mut problems: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        let mut pool: Vec<i32> = (1..top as i32 + 1).collect();
        for i in 0..n {
            let j = i + (next_random(&mut seed) % (top - i) as i64) as usize;
            pool.swap(i, j);
        }
        problems.push(pool[0..n].to_vec());
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in problems.iter() {
            let answer = tuple_same_product(nums) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!(
        "{} problems of {} values up to {}, {} rounds: answers sum to {}, checksum {}",
        count, n, top, rounds, sum, check
    );
}
