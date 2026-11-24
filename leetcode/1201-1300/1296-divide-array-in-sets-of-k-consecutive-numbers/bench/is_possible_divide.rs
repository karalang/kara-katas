// LeetCode #1296 bench: the ★ arm over 20 arrays of 16666 runs of 6
// consecutive numbers, shuffled, built once; then 10 passes, each swapping two
// numbers of every array and choosing k from the checksum so far. The counts
// are in a `BTreeMap`, as the ★ arm's are in a `SortedMap`.
use std::collections::BTreeMap;

fn is_possible_divide(nums: &[i64], k: i64) -> bool {
    if nums.len() as i64 % k != 0 {
        return false;
    }
    let mut count: BTreeMap<i64, i64> = BTreeMap::new();
    for &x in nums {
        *count.entry(x).or_insert(0) += 1;
    }
    let keys: Vec<i64> = count.keys().cloned().collect();
    for &x in keys.iter() {
        let sets = count[&x];
        if sets == 0 {
            continue;
        }
        for y in x..x + k {
            let have = count.get(&y).cloned().unwrap_or(0);
            if have < sets {
                return false;
            }
            count.insert(y, have - sets);
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 1296;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20 {
        let spread = if a % 2 == 0 { 10000 } else { 1000000000 };
        let mut nums = Vec::new();
        for _ in 0..16666 {
            let start = 1 + wide_random(&mut seed) % spread;
            for d in 0..6 {
                nums.push(start + d);
            }
        }
        let len = nums.len();
        for i in 0..len {
            let j = i + (wide_random(&mut seed) % (len - i) as i64) as usize;
            nums.swap(i, j);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..10 {
        for a in 0..arrays.len() {
            let len = arrays[a].len() as i64;
            let i = (check % len) as usize;
            let j = ((check / len) % len) as usize;
            arrays[a].swap(i, j);
            let k = 1 + check % 6;
            let possible = is_possible_divide(&arrays[a], k);
            check = (check * 31 + if possible { 2 } else { 1 } + p) % 1000000007;
        }
    }
    println!("10 passes over 20 arrays of 99996: checksum {}", check);
}
