// LeetCode #2239: Find Closest Number to Zero -- the benchmark's Rust
// mirror of closest.kara: one scan, a number kept when nearer to zero,
// or as near and larger.

fn find_closest_number(nums: &[i64]) -> i64 {
    let mut closest = nums[0];
    for &x in nums {
        if x.abs() < closest.abs() || (x.abs() == closest.abs() && x > closest) {
            closest = x;
        }
    }
    closest
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2239i64;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..1000 {
        nums.push(wide_random(&mut seed) % 200001 - 100000);
    }
    let mut check = 0i64;
    for _ in 0..100000 {
        // punch: one number drawn again before each pass
        let at = (next_random(&mut seed) % 1000) as usize;
        nums[at] = wide_random(&mut seed) % 200001 - 100000;
        check = (check * 31 + find_closest_number(&nums) + 100000) % 1000000007;
    }
    println!("100000 passes over 1000 numbers: checksum {}", check);
}
