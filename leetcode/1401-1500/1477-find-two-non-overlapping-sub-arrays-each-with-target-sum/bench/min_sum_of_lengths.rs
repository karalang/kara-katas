// LeetCode #1477: Find Two Non-overlapping Sub-arrays Each With Target
// Sum -- bench, Rust mirror of min_sum_of_lengths.kara

fn min_sum_of_lengths(arr: &[i32], target: i32) -> i32 {
    let n = arr.len() as i64;
    let none = n + 1;
    let mut shortest = vec![none; n as usize];
    let mut best = 2 * none;
    let mut sum: i64 = 0;
    let mut left: usize = 0;
    for right in 0..n as usize {
        sum += arr[right] as i64;
        while sum > target as i64 {
            sum -= arr[left] as i64;
            left += 1;
        }
        let mut here = none;
        if sum == target as i64 {
            here = (right - left + 1) as i64;
            if left > 0 && shortest[left - 1] < none {
                best = best.min(here + shortest[left - 1]);
            }
        }
        shortest[right] = if right > 0 { shortest[right - 1].min(here) } else { here };
    }
    if best >= 2 * none { -1 } else { best as i32 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1477;
    let mut arr: Vec<i32> = (0..100000).map(|_| (1 + next_random(&mut seed) % 1000) as i32).collect();
    let mut check: i64 = 0;
    for pass in 0..400i64 {
        arr[(check % 100000) as usize] = (1 + (check / 7) % 1000) as i32;
        let target = (500 + check % 20000) as i32;
        let got = min_sum_of_lengths(&arr, target);
        check = (check * 31 + got as i64 + 1 + pass) % 1000000007;
    }
    println!("400 passes over 100000 values: checksum {}", check);
}
