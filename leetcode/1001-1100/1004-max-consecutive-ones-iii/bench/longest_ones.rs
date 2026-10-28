// Benchmark: LeetCode #1004 Max Consecutive Ones III -- the ★ arm, a
// sliding window, on arrays of 100000 numbers, LeetCode's longest.
// Mirrors longest_ones.kara, .c, .py and go-seq/.

fn longest_ones(nums: &[i64], k: i64) -> i64 {
    let mut left = 0usize;
    let mut zeros = 0i64;
    let mut best = 0i64;
    for right in 0..nums.len() {
        if nums[right] == 0 {
            zeros += 1;
        }
        while zeros > k {
            if nums[left] == 0 {
                zeros -= 1;
            }
            left += 1;
        }
        best = best.max(right as i64 - left as i64 + 1);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 30;
    let n: i64 = 100000;
    let mut seed: i64 = 1004;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for t in 0..20i64 {
        let nums: Vec<i64> = (0..n)
            .map(|_| if next_random(&mut seed) % 8 < t % 7 + 1 { 1 } else { 0 })
            .collect();
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20i64 {
            let t = (r + i) % 20;
            let k = (r * 37 + t * 101) % 3000;
            let got = longest_ones(&arrays[t as usize], k);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 arrays of {n} numbers: answers sum to {total}, checksum {check}");
}
