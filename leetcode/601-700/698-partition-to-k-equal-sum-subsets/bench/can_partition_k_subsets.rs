// LeetCode #698: Partition to K Equal Sum Subsets -- bench program, Rust mirror of the bottom-up arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn can_partition_k_subsets(nums: &[i64], k: i64) -> bool {
    let n = nums.len();
    let total: i64 = nums.iter().sum();
    if total % k != 0 {
        return false;
    }
    let target = total / k;
    let size = 1usize << n;
    let mut fill: Vec<i64> = vec![-1; size];
    fill[0] = 0;
    for mask in 0..size {
        if fill[mask] < 0 {
            continue;
        }
        for i in 0..n {
            let next = mask | (1 << i);
            if next != mask && fill[next] < 0 && fill[mask] + nums[i] <= target {
                fill[next] = (fill[mask] + nums[i]) % target;
            }
        }
    }
    fill[size - 1] == 0
}

fn main() {
    let mut seed = 698;
    let mut problems: Vec<Vec<i64>> = Vec::new();
    let mut ks: Vec<i64> = Vec::new();
    for p in 0..100i64 {
        let k = 1i64 << (p % 5);
        let g = 16 / k;
        let target = 16 + next_random(&mut seed) % 9985;
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..k {
            let mut left = target;
            for _ in 0..g - 1 {
                let part = 1 + next_random(&mut seed) % (target / g);
                nums.push(part);
                left -= part;
            }
            nums.push(left);
        }
        for i in 0..16usize {
            let j = i + (next_random(&mut seed) % (16 - i as i64)) as usize;
            nums.swap(i, j);
        }
        if p % 2 == 1 {
            let i = (next_random(&mut seed) % 16) as usize;
            let j = ((i as i64 + 1 + next_random(&mut seed) % 15) % 16) as usize;
            let most = (nums[j] - 1).min(10000 - nums[i]);
            if most >= 1 {
                let d = 1 + next_random(&mut seed) % most;
                nums[i] += d;
                nums[j] -= d;
            }
        }
        problems.push(nums);
        ks.push(k);
    }
    let rounds = 2;
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for p in 0..problems.len() {
            let r = can_partition_k_subsets(&problems[p], ks[p]);
            if r {
                yes += 1;
            }
            checksum = (checksum * 3 + (if r { 1 } else { 0 }) + p as i64) % 1000000007;
        }
    }
    println!("{} rounds of 100 problems of 16 values: {} answers yes, checksum {}", rounds, yes, checksum);
}
