// LeetCode #1346 bench in Rust: the ★ arm (a `HashSet` of the values seen
// so far, each new value checked for its double and, when even, its half)
// on the same 2000 arrays of 500 values and 100 passes.
use std::collections::HashSet;

fn check_if_exist(arr: &[i32]) -> bool {
    let mut seen = HashSet::new();
    for &x in arr {
        if seen.contains(&(2 * x)) || (x % 2 == 0 && seen.contains(&(x / 2))) {
            return true;
        }
        seen.insert(x);
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1346;
    let mut arrays: Vec<Vec<i32>> = (0..2000)
        .map(|_| (0..500).map(|_| (2 * (next_random(&mut seed) % 1000) - 999) as i32).collect())
        .collect();
    let mut check: i64 = 0;
    for pass in 0..100 {
        for a in 0..2000 {
            arrays[a][(check % 500) as usize] = ((check / 7) % 2001 - 1000) as i32;
            let yes = check_if_exist(&arrays[a]);
            check = (check * 31 + if yes { 2 } else { 1 } + pass) % 1000000007;
        }
    }
    println!("100 passes over 2000 arrays of 500: checksum {}", check);
}
