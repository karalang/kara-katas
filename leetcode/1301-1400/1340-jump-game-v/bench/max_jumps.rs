// LeetCode #1340 bench in Rust: the ★ arm (memoized depth-first search,
// each direction walked outward up to d steps and stopped at the first
// value not lower) on the same 20 arrays of 1000 values and 20 passes.

fn most_from(arr: &[i32], d: i64, i: i64, memo: &mut Vec<i32>) -> i32 {
    if memo[i as usize] > 0 {
        return memo[i as usize];
    }
    let n = arr.len() as i64;
    let mut best = 1;
    for step in [-1i64, 1] {
        let mut j = i + step;
        while j >= 0 && j < n && (j - i).abs() <= d && arr[j as usize] < arr[i as usize] {
            best = best.max(1 + most_from(arr, d, j, memo));
            j += step;
        }
    }
    memo[i as usize] = best;
    best
}

fn max_jumps(arr: &[i32], d: i64) -> i32 {
    let mut memo = vec![0; arr.len()];
    let mut best = 0;
    for i in 0..arr.len() as i64 {
        best = best.max(most_from(arr, d, i, &mut memo));
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 1000usize;
    let mut seed = 1340;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for a in 0..20 {
        let mut arr = Vec::with_capacity(n);
        for k in 0..n as i64 {
            if a % 2 == 0 {
                arr.push((1 + next_random(&mut seed) % 100000) as i32);
            } else {
                arr.push((100 * k + 1 + next_random(&mut seed) % 100) as i32);
            }
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for pass in 0..20 {
        for a in 0..20 {
            arrays[a][(check % n as i64) as usize] = (1 + (check / 7) % 100000) as i32;
            let d = if a % 2 == 0 { 1000 } else { 300 };
            let answer = max_jumps(&arrays[a], d);
            check = (check * 31 + answer as i64 + pass) % 1000000007;
        }
    }
    println!("20 passes over 20 arrays of 1000: checksum {}", check);
}
