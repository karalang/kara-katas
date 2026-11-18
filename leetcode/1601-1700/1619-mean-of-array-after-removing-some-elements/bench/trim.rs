// LeetCode #1619: Mean of Array After Removing Some Elements -- the bench in
// Rust, mirroring trim.kara: sort a copy, then the mean of the middle 90%.

fn trim_mean(arr: &[i32]) -> f64 {
    let mut sorted = arr.to_vec();
    sorted.sort();
    let k = sorted.len() / 20;
    let kept = &sorted[k..sorted.len() - k];
    kept.iter().map(|&x| x as i64).sum::<i64>() as f64 / kept.len() as f64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1619;
    let arrays: Vec<Vec<i32>> = (0..20000)
        .map(|_| {
            (0..1000)
                .map(|_| ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100001) as i32)
                .collect()
        })
        .collect();
    let mut check: i64 = 0;
    let mut total = 0.0;
    for arr in &arrays {
        let mean = trim_mean(arr);
        total += mean;
        check = (check * 31 + (mean * 100000.0).round() as i64 + 1) % 1000000007;
    }
    println!("20000 arrays of 1000 values: means sum to {total:.5}, checksum {check}");
}
