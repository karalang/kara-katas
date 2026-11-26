// LeetCode #1785: Minimum Elements to Add to Form a Given Sum -- the bench
// in Rust, mirroring min_elements.kara: the gap over the limit, rounded up.

fn min_elements(nums: &[i32], limit: i32, goal: i32) -> i32 {
    let sum: i64 = nums.iter().map(|&x| x as i64).sum();
    let gap = (goal as i64 - sum).abs();
    ((gap + limit as i64 - 1) / limit as i64) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1785;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..4000 {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..100 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            nums.push(((a * 32768 + b) % 2000001 - 1000000) as i32);
        }
        lists.push(nums);
    }
    let mut check: i64 = 0;
    for call in 0..6000000i64 {
        let nums = &lists[((check + call) % 4000) as usize];
        let limit = 1 + (check + call) % 1000000;
        let goal = check % 2000000001 - 1000000000;
        check = (check * 31 + min_elements(nums, limit as i32, goal as i32) as i64) % 1000000007;
    }
    println!("6000000 calls over 4000 lists: checksum {}", check);
}
