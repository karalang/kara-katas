// LeetCode #1711: Count Good Meals -- the Rust mirror of the bench
// (meals.kara): one pass, each dish paired with the earlier dishes that
// make each of the 22 powers with it, counted in a `HashMap`, on 10
// random lists of 100000 dishes, each answered 3 times.

use std::collections::HashMap;

fn count_pairs(deliciousness: &[i32]) -> i32 {
    let mut seen: HashMap<i32, i64> = HashMap::new();
    let mut pairs: i64 = 0;
    for &d in deliciousness.iter() {
        for b in 0..22 {
            pairs += seen.get(&((1 << b) - d)).copied().unwrap_or(0);
        }
        *seen.entry(d).or_insert(0) += 1;
    }
    (pairs % 1000000007) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let rounds: i64 = 3;
    let n = 100000;
    let top: i64 = 1 << 20;
    let mut seed: i64 = 1711;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        let mut list = Vec::with_capacity(n);
        for _ in 0..n {
            let a = next_random(&mut seed);
            list.push(((a * 32768 + next_random(&mut seed)) % (top + 1)) as i32);
        }
        lists.push(list);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for deliciousness in lists.iter() {
            let answer = count_pairs(deliciousness) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} lists of {n} dishes, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
