// LeetCode #2035: Partition Array Into Two Arrays to Minimize Sum
// Difference -- the ★ arm in Rust, the same algorithm and workload as
// partition.kara: each half's subset sums listed by size, the right lists
// sorted (`sort`, as Kāra's), and `partition_point` for the right sum that
// brings the side to half the total, with the sums on either side tried.

fn subset_sums(half: &[i64]) -> Vec<Vec<i64>> {
    let n = half.len();
    let mut by_size: Vec<Vec<i64>> = vec![Vec::new(); n + 1];
    for mask in 0..1i64 << n {
        let mut sum = 0;
        let mut size = 0;
        for i in 0..n {
            if mask >> i & 1 == 1 {
                sum += half[i];
                size += 1;
            }
        }
        by_size[size].push(sum);
    }
    by_size
}

fn minimum_difference(nums: &[i64]) -> i64 {
    let n = nums.len() / 2;
    let total: i64 = nums.iter().sum();
    let left = subset_sums(&nums[0..n]);
    let mut right = subset_sums(&nums[n..2 * n]);
    for list in right.iter_mut() {
        list.sort();
    }
    let mut best = i64::MAX;
    for k in 0..n + 1 {
        let others = &right[n - k];
        for &a in left[k].iter() {
            let at = others.partition_point(|&b| 2 * (a + b) < total);
            if at < others.len() {
                best = best.min((total - 2 * (a + others[at])).abs());
            }
            if at > 0 {
                best = best.min((total - 2 * (a + others[at - 1])).abs());
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2035;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..40 {
        let top = [10000000, 1000, 100, 10000000, 50][a % 5];
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..30 {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            nums.push((hi * 32768 + lo) % (2 * top + 1) - top);
        }
        arrays.push(nums);
    }
    let mut calls = 0;
    let mut sum = 0;
    let mut check = 0;
    for round in 0..5 {
        for a in 0..40 {
            let at = (round * 7 + a * 3) % 30;
            arrays[a][at] = -arrays[a][at];
            let answer = minimum_difference(&arrays[a]);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
