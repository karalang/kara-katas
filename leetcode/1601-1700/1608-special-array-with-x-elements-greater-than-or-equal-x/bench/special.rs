// LeetCode #1608: Special Array With X Elements Greater Than or Equal X --
// the bench in Rust, mirroring special.kara: the numbers sorted largest
// first, `x` special when the `x`th largest is at least `x` and the next
// is below it.

fn special_array(mut nums: Vec<i32>) -> i32 {
    nums.sort_by(|a, b| b.cmp(a));
    let n = nums.len();
    for x in 1..=n {
        if nums[x - 1] as usize >= x && (x == n || (nums[x] as usize) < x) {
            return x as i32;
        }
    }
    -1
}

fn main() {
    let mut seed: i64 = 1608;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut problems: Vec<Vec<i32>> = Vec::new();
    for _ in 0..1000 {
        let mut nums = Vec::with_capacity(10000);
        for _ in 0..10000 {
            let a = next_random();
            let b = next_random();
            nums.push(((a * 32768 + b) % 10001) as i32);
        }
        problems.push(nums);
    }
    let mut check: i64 = 0;
    let mut special = 0;
    for nums in &problems {
        let x = special_array(nums.clone());
        if x >= 0 {
            special += 1;
        }
        check = (check * 31 + x as i64 + 1) % 1000000007;
    }
    println!("1000 problems of 10000 numbers from 0 to 10000: {special} special, checksum {check}");
}
