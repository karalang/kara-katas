// LeetCode #719: Find K-th Smallest Pair Distance -- binary search on
// the distance. Benchmark mirror of the Kara star arm: sort a copy,
// then find the least distance with at least k pairs, counting pairs
// with two pointers.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn smallest_distance_pair(nums: &[i64], k: i64) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let n = sorted.len();
    let mut lo = 0;
    let mut hi = sorted[n - 1] - sorted[0];
    while lo < hi {
        let mid = (lo + hi) / 2;
        let mut count = 0i64;
        let mut left = 0;
        for right in 0..n {
            while sorted[right] - sorted[left] > mid {
                left += 1;
            }
            count += (right - left) as i64;
        }
        if count >= k {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    let mut seed: i64 = 719;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..40 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..5000 {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            nums.push((hi * 32768 + lo) % 1000001);
        }
        arrays.push(nums);
    }
    let pairs: i64 = 5000 * 4999 / 2;
    let mut sum = 0;
    for round in 0..25i64 {
        for a in 0..40i64 {
            let k = 1 + (round * 7919 + a * 104729) % pairs;
            sum += smallest_distance_pair(&arrays[a as usize], k);
        }
    }
    println!("25 rounds of 40 arrays of 5000 numbers: sum {}", sum);
}
