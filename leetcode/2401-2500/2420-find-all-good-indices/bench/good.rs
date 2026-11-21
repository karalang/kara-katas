// LeetCode #2420: Find All Good Indices -- the bench, the ★ arm: the run of
// values ending at each index without rising, from the left, and the run
// starting at each index without falling, from the right.

fn good_indices(nums: &[i64], k: usize) -> Vec<usize> {
    let n = nums.len();
    let mut falling = vec![1usize; n];
    let mut rising = vec![1usize; n];
    for i in 1..n {
        if nums[i] <= nums[i - 1] {
            falling[i] = falling[i - 1] + 1;
        }
    }
    for i in (0..n - 1).rev() {
        if nums[i] <= nums[i + 1] {
            rising[i] = rising[i + 1] + 1;
        }
    }
    let mut good = Vec::new();
    for i in k..n - k {
        if falling[i - 1] >= k && rising[i + 1] >= k {
            good.push(i);
        }
    }
    good
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2420;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut nums: Vec<i64> = Vec::new();
        let mut down = true;
        for i in 0..100000 {
            if i == 0 {
                nums.push(1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000);
            } else {
                if next_random(&mut seed) % 60 == 0 {
                    down = !down;
                }
                let d = next_random(&mut seed) % 41;
                let v = if down { nums[i - 1] - d } else { nums[i - 1] + d };
                nums.push(v.max(1).min(1000000));
            }
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..100 {
        for a in 0..10 {
            let good = good_indices(&arrays[a], 1 + (p + a) % 40);
            let sum: usize = good.iter().sum();
            check = (check * 31 + good.len() as i64 + (sum % 1000003) as i64) % 1000000007;
        }
    }
    println!("100 passes over 10 arrays of 10^5 values: checksum {}", check);
}
