// LeetCode #2454: Next Greater Element IV -- bench, Rust mirror of
// second.kara: two monotonic stacks, the first waiting for one greater
// value and the second for another.

fn second_greater_element(nums: &[i64]) -> Vec<i64> {
    let n = nums.len();
    let mut answer = vec![-1i64; n];
    let mut first: Vec<usize> = Vec::new();
    let mut second: Vec<usize> = Vec::new();
    for j in 0..n {
        while !second.is_empty() && nums[second[second.len() - 1]] < nums[j] {
            answer[second.pop().unwrap()] = nums[j];
        }
        let mut cut = first.len();
        while cut > 0 && nums[first[cut - 1]] < nums[j] {
            cut -= 1;
        }
        for i in cut..first.len() {
            second.push(first[i]);
        }
        first.truncate(cut);
        first.push(j);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let mut seed: i64 = 2454;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let hi = next_random(&mut seed);
            nums.push((hi * 32768 + next_random(&mut seed)) % 1000000001);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..20i64 {
        for a in 0..10i64 {
            arrays[a as usize][((p * 7919 + a) % n) as usize] = check % 1000000001;
            for v in second_greater_element(&arrays[a as usize]) {
                check = (check * 31 + v + 1) % 1000000007;
            }
            check = (check + p) % 1000000007;
        }
    }
    println!("20 passes over 10 arrays of 10^5 values: checksum {}", check);
}
