// LeetCode #1589: Maximum Sum Obtained of Any Permutation -- the bench in
// Rust, mirroring max_sum.kara. Each request is its own `Vec`.

fn max_sum_range_query(nums: &[i32], requests: &[Vec<i32>]) -> i32 {
    let n = nums.len();
    let mut asked = vec![0i64; n + 1];
    for r in requests {
        asked[r[0] as usize] += 1;
        asked[r[1] as usize + 1] -= 1;
    }
    for i in 1..n {
        asked[i] += asked[i - 1];
    }
    asked.truncate(n);
    asked.sort();
    let mut values = nums.to_vec();
    values.sort();
    let mut total = 0i64;
    for (count, v) in asked.iter().zip(values.iter()) {
        total = (total + count * *v as i64) % 1000000007;
    }
    total as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 1589;
    let n = 100000;
    let mut problems = Vec::new();
    for _ in 0..20 {
        let nums: Vec<i32> = (0..n).map(|_| (wide(&mut seed) % 100001) as i32).collect();
        let mut requests: Vec<Vec<i32>> = Vec::new();
        for _ in 0..100000 {
            let a = wide(&mut seed) % n;
            let b = wide(&mut seed) % n;
            requests.push(vec![a.min(b) as i32, a.max(b) as i32]);
        }
        problems.push((nums, requests));
    }
    let mut check: i64 = 0;
    for (nums, requests) in &problems {
        check = (check * 31 + max_sum_range_query(nums, requests) as i64 + 1) % 1000000007;
    }
    println!("20 problems of 100000 values and 100000 requests: checksum {}", check);
}
