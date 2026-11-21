// LeetCode #2448: Minimum Cost to Make Array Equal -- the bench, the ★
// arm: the pairs sorted, the weighted median the first value whose
// running cost reaches half the total, and every value moved there.

fn min_cost(nums: &[i64], cost: &[i64]) -> i64 {
    let mut pairs: Vec<(i64, i64)> = nums.iter().cloned().zip(cost.iter().cloned()).collect();
    pairs.sort();
    let total: i64 = cost.iter().sum();
    let mut running = 0;
    let mut target = 0;
    for &(value, c) in pairs.iter() {
        running += c;
        if 2 * running >= total {
            target = value;
            break;
        }
    }
    let mut answer = 0;
    for i in 0..nums.len() {
        answer += (nums[i] - target).abs() * cost[i];
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2448;
    let n: usize = 100000;
    let mut nums: Vec<i64> = Vec::new();
    let mut cost: Vec<i64> = Vec::new();
    for _ in 0..n {
        let r = next_random(&mut seed);
        nums.push(1 + (r * 32768 + next_random(&mut seed)) % 1000000);
        let r = next_random(&mut seed);
        cost.push(1 + (r * 32768 + next_random(&mut seed)) % 1000000);
    }
    let mut check: i64 = 0;
    for p in 0..200usize {
        for t in 0..1000 {
            cost[(1000 * p + t) % n] = 1 + next_random(&mut seed) * 30;
        }
        check = (check * 31 + min_cost(&nums, &cost) % 1000000007 + p as i64) % 1000000007;
    }
    println!("200 passes over 10^5 values: checksum {}", check);
}
