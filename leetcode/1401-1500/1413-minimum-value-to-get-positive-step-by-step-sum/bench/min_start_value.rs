fn min_start_value(nums: &[i32]) -> i32 {
    let mut sum: i32 = 0;
    let mut lowest: i32 = 0;
    for &x in nums.iter() {
        sum += x;
        lowest = lowest.min(sum);
    }
    1 - lowest
}

fn main() {
    let mut seed: i64 = 1413;
    let mut pool: Vec<i32> = Vec::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push((seed / 65536 % 201 - 100) as i32);
    }
    let mut check: i64 = 0;
    for _ in 0..3000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (seed / 65536 % 99901) as usize;
        check = (check * 131 + min_start_value(&pool[start..start + 100]) as i64) % 1000000007;
    }
    println!("3 * 10^6 windows of 100 numbers: checksum {}", check);
}
