// LeetCode #2439: Minimize Maximum of Array -- the bench, the ★ arm: the
// largest ceiling average of any prefix, in one pass.

fn minimize_array_value(nums: &[i64]) -> i64 {
    let mut sum = 0i64;
    let mut answer = 0i64;
    for i in 0..nums.len() {
        sum += nums[i];
        let k = i as i64;
        answer = answer.max((sum + k) / (k + 1));
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    (a * 32768 + next_random(seed)) % 1000000001
}

fn main() {
    let mut seed = 2439i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            nums.push(wide(&mut seed));
        }
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..100i64 {
        for c in 0..arrays.len() {
            let at = ((p * 7919 + c as i64 * 104729) % 100000) as usize;
            arrays[c][at] = wide(&mut seed);
            check = (check * 31 + minimize_array_value(&arrays[c]) + p) % 1000000007;
        }
    }
    println!("100 passes over 10 arrays of 10^5 values: checksum {}", check);
}
