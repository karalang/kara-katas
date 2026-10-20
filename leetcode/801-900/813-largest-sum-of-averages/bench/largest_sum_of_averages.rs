// LeetCode 813 -- Largest Sum of Averages: the bench, with the ★ arm's one
// row of prefix-sum DP.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn largest_sum_of_averages(nums: &[i64], k: i64) -> f64 {
    let n = nums.len();
    let mut prefix = vec![0i64; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    let mut best = vec![0.0f64; n + 1];
    for i in 1..=n {
        best[i] = prefix[i] as f64 / i as f64;
    }
    for _ in 1..k {
        let mut i = n;
        while i >= 1 {
            for p in 1..i {
                let candidate = best[p] + (prefix[i] - prefix[p]) as f64 / (i - p) as f64;
                if candidate > best[i] {
                    best[i] = candidate;
                }
            }
            i -= 1;
        }
    }
    best[n]
}

// 64 arrays of 100 numbers from 1 to 10000 are made once. Each round writes
// a new number into one place of the next array and finds its largest sum
// of averages in at most k groups, k going round 1 to 100.
fn main() {
    let mut seed = 813;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..64 {
        let mut nums = Vec::new();
        for _ in 0..100 {
            nums.push(1 + next_random(&mut seed) % 10000);
        }
        arrays.push(nums);
    }
    let rounds: i64 = 6000;
    let mut total = 0.0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let a = (r % 64) as usize;
        arrays[a][(r / 64 % 100) as usize] = 1 + next_random(&mut seed) % 10000;
        let answer = largest_sum_of_averages(&arrays[a], 1 + r % 100);
        total += answer;
        check = (check * 131 + (answer * 1000.0) as i64) % 1000000007;
    }
    println!("{} rounds of 100 numbers: total {:.5}, checksum {}", rounds, total, check);
}
