// Benchmark for #659: the greedy, as the Kara ★ arm.
use std::collections::HashMap;

fn count(m: &HashMap<i64, i64>, k: i64) -> i64 {
    *m.get(&k).unwrap_or(&0)
}

fn is_possible(nums: &[i64]) -> bool {
    let mut left: HashMap<i64, i64> = HashMap::new();
    for &x in nums {
        *left.entry(x).or_insert(0) += 1;
    }
    let mut ends: HashMap<i64, i64> = HashMap::new();
    for &x in nums {
        if count(&left, x) == 0 {
            continue;
        }
        *left.entry(x).or_insert(0) -= 1;
        if count(&ends, x - 1) > 0 {
            *ends.entry(x - 1).or_insert(0) -= 1;
            *ends.entry(x).or_insert(0) += 1;
        } else if count(&left, x + 1) > 0 && count(&left, x + 2) > 0 {
            *left.entry(x + 1).or_insert(0) -= 1;
            *left.entry(x + 2).or_insert(0) -= 1;
            *ends.entry(x + 2).or_insert(0) += 1;
        } else {
            return false;
        }
    }
    true
}

fn main() {
    let inputs = 8usize;
    let rounds = 40usize;
    let mut seed: i64 = 659;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for k in 0..inputs {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..25000 {
            let start = next_random() % 20001;
            let length = 3 + next_random() % 3;
            for v in start..start + length {
                nums.push(v);
            }
        }
        if k % 2 == 1 {
            nums.push(30000);
        }
        nums.sort();
        arrays.push(nums);
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let pick = (r * 3) % inputs;
        let ok = is_possible(&arrays[pick]);
        if ok {
            yes += 1;
        }
        checksum = (checksum * 31 + arrays[pick].len() as i64 * 2 + if ok { 1 } else { 0 }) % 1000000007;
    }
    println!("{} arrays, {} rounds: {} split, checksum {}", inputs, rounds, yes, checksum);
}
