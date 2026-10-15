// Benchmark for #644: mirror of max_average_ii.kara (the ★ arm: binary
// search on the average) on the same workload.

// The start and end of a subarray of `k` or more values averaging at
// least `m`, or (-1, -1) if there is none.
fn reaches(prefix: &[i64], k: i64, m: f64) -> (i64, i64) {
    let mut lowest: i64 = 0;
    for end in k..prefix.len() as i64 {
        let c = end - k;
        if ((prefix[c as usize] - prefix[lowest as usize]) as f64) < m * (c - lowest) as f64 {
            lowest = c;
        }
        if ((prefix[end as usize] - prefix[lowest as usize]) as f64) >= m * (end - lowest) as f64 {
            return (lowest, end);
        }
    }
    (-1, -1)
}

fn find_max_average(nums: &[i64], k: i64) -> f64 {
    let mut prefix: Vec<i64> = vec![0];
    for x in nums.iter() {
        prefix.push(prefix[prefix.len() - 1] + *x);
    }
    let mut lo = nums[0] as f64;
    let mut hi = nums[0] as f64;
    for x in nums.iter() {
        lo = lo.min(*x as f64);
        hi = hi.max(*x as f64);
    }
    let mut best = (0i64, nums.len() as i64);
    for _ in 0..100 {
        let mid = (lo + hi) / 2.0;
        let (start, end) = reaches(&prefix, k, mid);
        if start == -1 {
            hi = mid;
        } else {
            lo = mid;
            best = (start, end);
        }
    }
    let (start, end) = best;
    (prefix[end as usize] - prefix[start as usize]) as f64 / (end - start) as f64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 644;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            nums.push(next_random(&mut seed) % 20001 - 10000);
        }
        arrays.push(nums);
    }
    let rounds: i64 = 40;
    let mut total = 0.0;
    for r in 0..rounds {
        let k = 1 + (r * 7919) % 100000;
        total += find_max_average(&arrays[(r % 20) as usize], k);
    }
    println!("{} rounds over 20 arrays of 100000 values: answers adding to {:.5}", rounds, total);
}
