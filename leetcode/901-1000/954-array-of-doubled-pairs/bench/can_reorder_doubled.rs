// LeetCode #954: Array of Doubled Pairs -- Rust mirror of the Kara bench
// program (counts, smallest first).
use std::collections::HashMap;

fn can_reorder_doubled(arr: &[i64]) -> bool {
    let mut count: HashMap<i64, i64> = HashMap::new();
    for &x in arr {
        *count.entry(x).or_insert(0) += 1;
    }
    let mut values: Vec<i64> = count.keys().copied().collect();
    values.sort_by_key(|x| x.abs());
    for &x in &values {
        let c = *count.get(&x).unwrap_or(&0);
        if c == 0 {
            continue;
        }
        if x == 0 {
            if c % 2 != 0 {
                return false;
            }
            continue;
        }
        let d = *count.get(&(2 * x)).unwrap_or(&0);
        if d < c {
            return false;
        }
        count.insert(2 * x, d - c);
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 10;
    let count = 20;
    let n = 30000usize;
    let mut seed = 954i64;
    let mut sets: Vec<Vec<i64>> = Vec::new();
    for s in 0..count {
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..n / 2 {
            let a = next_random(&mut seed);
            let x = (a * 32768 + next_random(&mut seed)) % 100001 - 50000;
            arr.push(x);
            arr.push(2 * x);
        }
        for i in 0..n {
            let a = next_random(&mut seed);
            let j = i + ((a * 32768 + next_random(&mut seed)) % (n - i) as i64) as usize;
            arr.swap(i, j);
        }
        if s % 4 == 3 {
            arr[s * 1000] = 2 * (arr[s * 1000] / 2) + 1;
        }
        sets.push(arr);
    }
    let mut yes = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for i in 0..count {
            let k = (r + i) % count;
            let ok = can_reorder_doubled(&sets[k]);
            if ok {
                yes += 1;
            }
            check = (check * 31 + if ok { 1 } else { 2 }) % 1000000007;
        }
    }
    println!("{} rounds over {} sets of {} values: {} can be paired, checksum {}", rounds, count, n, yes, check);
}
