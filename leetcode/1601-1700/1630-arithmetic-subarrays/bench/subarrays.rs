// LeetCode #1630: Arithmetic Subarrays -- the bench's Rust mirror: the ★
// arm on 200 random problems of 500 numbers and 500 queries, all drawn
// first.

fn check_arithmetic_subarrays(nums: &[i32], l: &[i32], r: &[i32]) -> Vec<bool> {
    l.iter()
        .zip(r.iter())
        .map(|(&a, &b)| {
            let mut run = nums[a as usize..=b as usize].to_vec();
            run.sort();
            let step = run[1] - run[0];
            run.windows(2).all(|pair| pair[1] - pair[0] == step)
        })
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1630;
    let mut problems: Vec<(Vec<i32>, Vec<i32>, Vec<i32>)> = Vec::new();
    for p in 0..200 {
        let mut nums: Vec<i32> = Vec::new();
        for i in 0..500i64 {
            if p % 2 == 0 {
                nums.push((3 * i - 700) as i32);
            } else {
                nums.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 200001 - 100000) as i32);
            }
        }
        for i in (1..500usize).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            nums.swap(i, j);
        }
        let mut l = Vec::new();
        let mut r = Vec::new();
        for _ in 0..500 {
            let a = next_random(&mut seed) % 499;
            l.push(a as i32);
            r.push((a + 1 + next_random(&mut seed) % (499 - a)) as i32);
        }
        problems.push((nums, l, r));
    }
    let mut check: i64 = 0;
    let mut yes = 0;
    for (nums, l, r) in &problems {
        for answer in check_arithmetic_subarrays(nums, l, r) {
            if answer {
                yes += 1;
            }
            check = (check * 31 + answer as i64 + 1) % 1000000007;
        }
    }
    println!("200 problems of 500 numbers and 500 queries: {} arithmetic, checksum {}", yes, check);
}
