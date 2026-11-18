// LeetCode #2321: Maximum Score Of Spliced Array -- the bench, the ★ arm
// in Rust. Each array's sum plus the largest subarray sum of the
// differences the other array would bring, by Kadane's walk, both ways
// round. O(n).

fn best_gain(into: &[i64], from: &[i64]) -> i64 {
    let mut best = 0;
    let mut here = 0;
    for i in 0..into.len() {
        here = (here + from[i] - into[i]).max(0);
        best = best.max(here);
    }
    best
}

fn maximums_spliced_array(nums1: &[i64], nums2: &[i64]) -> i64 {
    let sum1: i64 = nums1.iter().sum();
    let sum2: i64 = nums2.iter().sum();
    (sum1 + best_gain(nums1, nums2)).max(sum2 + best_gain(nums2, nums1))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let mut seed: i64 = 2321;
    let mut firsts: Vec<Vec<i64>> = Vec::new();
    let mut seconds: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        firsts.push((0..n).map(|_| next_random(&mut seed) % 10000 + 1).collect());
        seconds.push((0..n).map(|_| next_random(&mut seed) % 10000 + 1).collect());
    }
    let mut check: i64 = 0;
    for _ in 0..200 {
        for k in 0..10 {
            let i = (next_random(&mut seed) % n) as usize;
            firsts[k][i] = next_random(&mut seed) % 10000 + 1;
            check = (check * 31 + maximums_spliced_array(&firsts[k], &seconds[k])) % 1000000007;
        }
    }
    println!("200 passes over 10 pairs of 10^5 numbers: checksum {}", check);
}
