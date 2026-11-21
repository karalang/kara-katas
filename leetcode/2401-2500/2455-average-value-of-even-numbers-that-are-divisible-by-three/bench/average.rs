// LeetCode #2455: Average Value of Even Numbers That Are Divisible by
// Three -- bench, Rust mirror of average.kara: one pass sums and counts
// the values divisible by 6.

fn average_value(nums: &[i64]) -> i64 {
    let mut sum = 0;
    let mut count = 0;
    for &x in nums {
        if x % 6 == 0 {
            sum += x;
            count += 1;
        }
    }
    if count == 0 { 0 } else { sum / count }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2455;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let nums: Vec<i64> = (0..1000).map(|_| 1 + next_random(&mut seed) % 1000).collect();
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..250i64 {
        for a in 0..1000i64 {
            arrays[a as usize][((p * 7919 + a) % 1000) as usize] = 1 + check % 1000;
            check = (check * 31 + average_value(&arrays[a as usize]) + p) % 1000000007;
        }
    }
    println!("250 passes over 1000 arrays of 1000 values: checksum {}", check);
}
