// Benchmark for #666: a map of places, walked from the root, as the Kara
// ★ arm.
use std::collections::HashMap;

fn path_sum(nums: &[i64]) -> i64 {
    let mut values: HashMap<i64, i64> = HashMap::new();
    for x in nums {
        values.insert(x / 10, x % 10);
    }
    walk(&values, 11, 0)
}

fn walk(values: &HashMap<i64, i64>, key: i64, above: i64) -> i64 {
    match values.get(&key) {
        None => 0,
        Some(v) => {
            let sum = above + v;
            let depth = key / 10;
            let position = key % 10;
            let left = (depth + 1) * 10 + 2 * position - 1;
            let right = left + 1;
            if !values.contains_key(&left) && !values.contains_key(&right) {
                sum
            } else {
                walk(values, left, sum) + walk(values, right, sum)
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(levels: i64, chance: i64, seed: &mut i64) -> Vec<i64> {
    let mut nums = vec![110 + next_random(seed) % 10];
    let mut level = vec![1i64];
    for depth in 2..levels + 1 {
        let mut next = Vec::new();
        for &p in &level {
            for c in 2 * p - 1..2 * p + 1 {
                if next_random(seed) % 100 < chance {
                    next.push(c);
                    nums.push(depth * 100 + c * 10 + next_random(seed) % 10);
                }
            }
        }
        level = next;
    }
    nums
}

fn main() {
    let mut seed: i64 = 666;
    let mut trees: Vec<Vec<i64>> = Vec::new();
    for _ in 0..256 {
        let chance = 50 + next_random(&mut seed) % 51;
        trees.push(random_tree(4, chance, &mut seed));
    }
    let rounds = 1000000i64;
    let mut sum = 0i64;
    for r in 0..rounds {
        sum = (sum * 31 + path_sum(&trees[(r % 256) as usize]) + r) % 1000000007;
    }
    println!("256 trees, {} rounds: checksum {}", rounds, sum);
}
