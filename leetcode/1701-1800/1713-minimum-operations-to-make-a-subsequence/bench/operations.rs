// LeetCode #1713: Minimum Operations to Make a Subsequence -- the Rust
// mirror of the bench (operations.kara): a `HashMap` of the target's
// places and the smallest tail of each rising run, found with
// `partition_point`, on 20 random problems of 100000 values, each answered
// 5 times.

use std::collections::HashMap;

fn min_operations(target: &[i32], arr: &[i32]) -> i32 {
    let mut place: HashMap<i32, i64> = HashMap::new();
    for (i, &v) in target.iter().enumerate() {
        place.insert(v, i as i64);
    }
    let mut tails: Vec<i64> = Vec::new();
    for a in arr.iter() {
        if let Some(&p) = place.get(a) {
            let i = tails.partition_point(|&t| t < p);
            if i == tails.len() {
                tails.push(p);
            } else {
                tails[i] = p;
            }
        }
    }
    (target.len() - tails.len()) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 20;
    let rounds: i64 = 5;
    let n: i64 = 100000;
    let mut seed: i64 = 1713;
    let mut problems: Vec<(Vec<i32>, Vec<i32>)> = Vec::new();
    for _ in 0..count {
        let mut target: Vec<i32> = (0..n).map(|v| v as i32).collect();
        for i in (1..n).rev() {
            let j = wide(&mut seed) % (i + 1);
            target.swap(i as usize, j as usize);
        }
        for i in 0..n as usize {
            target[i] = target[i] * 10000 + (next_random(&mut seed) % 10000) as i32;
        }
        let mut arr: Vec<i32> = Vec::new();
        for _ in 0..n {
            if next_random(&mut seed) % 2 == 0 {
                arr.push(target[(wide(&mut seed) % n) as usize]);
            } else {
                arr.push((wide(&mut seed) % 1000000000) as i32);
            }
        }
        problems.push((target, arr));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (target, arr) in problems.iter() {
            let answer = min_operations(target, arr) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} problems of {n} values, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
