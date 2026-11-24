// LeetCode #1343 bench in Rust: the ★ arm (a sliding window of the last k
// values, counted when its sum reaches k * threshold) on the same 10
// arrays of 10^5 values and 60 passes.

fn num_of_subarrays(arr: &[i32], k: i32, threshold: i32) -> i32 {
    let need = k * threshold;
    let k = k as usize;
    let mut sum = 0;
    let mut count = 0;
    for i in 0..arr.len() {
        sum += arr[i];
        if i >= k {
            sum -= arr[i - k];
        }
        if i + 1 >= k && sum >= need {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 100000usize;
    let mut seed = 1343;
    let mut arrays: Vec<Vec<i32>> = (0..10)
        .map(|_| (0..n).map(|_| (1 + next_random(&mut seed) % 10000) as i32).collect())
        .collect();
    let mut check: i64 = 0;
    for pass in 0..60 {
        for a in 0..10 {
            arrays[a][(check % n as i64) as usize] = (1 + (check / 7) % 10000) as i32;
            let k = (1 + check % 1000) as i32;
            let threshold = (4500 + check % 400) as i32;
            let answer = num_of_subarrays(&arrays[a], k, threshold);
            check = (check * 31 + answer as i64 + pass) % 1000000007;
        }
    }
    println!("60 passes over 10 arrays of 10^5: checksum {}", check);
}
