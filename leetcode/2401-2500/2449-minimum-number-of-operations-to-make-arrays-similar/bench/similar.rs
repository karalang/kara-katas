// LeetCode #2449: Minimum Number of Operations to Make Arrays Similar --
// the bench, the ★ arm: the odd and the even values of each array sorted
// and matched in order, the distance over 4.

fn make_similar(nums: &[i64], target: &[i64]) -> i64 {
    let mut odd: Vec<i64> = Vec::new();
    let mut even: Vec<i64> = Vec::new();
    for &x in nums.iter() {
        if x % 2 == 1 { odd.push(x) } else { even.push(x) }
    }
    let mut odd_target: Vec<i64> = Vec::new();
    let mut even_target: Vec<i64> = Vec::new();
    for &x in target.iter() {
        if x % 2 == 1 { odd_target.push(x) } else { even_target.push(x) }
    }
    odd.sort();
    even.sort();
    odd_target.sort();
    even_target.sort();
    let mut distance = 0;
    for i in 0..odd.len() {
        distance += (odd[i] - odd_target[i]).abs();
    }
    for i in 0..even.len() {
        distance += (even[i] - even_target[i]).abs();
    }
    distance / 4
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let r = next_random(seed);
    r * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2449;
    let n: i64 = 100000;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(1 + wide_random(&mut seed) % 1000000);
    }
    let mut target = nums.clone();
    let mut check: i64 = 0;
    for p in 0..220 {
        for _ in 0..1000 {
            let i = (wide_random(&mut seed) % n) as usize;
            let j = (wide_random(&mut seed) % n) as usize;
            let step = 2 * (1 + next_random(&mut seed) % 50);
            if i != j && target[i] + step <= 1000000 && target[j] - step >= 1 {
                target[i] += step;
                target[j] -= step;
            }
        }
        check = (check * 31 + make_similar(&nums, &target) + p) % 1000000007;
    }
    println!("220 passes over 10^5 values: checksum {}", check);
}
