// Benchmark for #396: mirror of rotate_function.kara (one rotation from the last).

fn max_rotate_function(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut sum = 0;
    let mut f = 0;
    for i in 0..n {
        sum += nums[i as usize];
        f += i * nums[i as usize];
    }
    let mut best = f;
    for k in 1..n {
        f = f + sum - n * nums[(n - k) as usize];
        best = best.max(f);
    }
    best
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let windows = 2000;
    let mut seed: i64 = 396;
    let mut pool: Vec<i64> = Vec::with_capacity(1000000);
    for _ in 0..1000000 {
        pool.push(step(&mut seed) % 201 - 100);
    }
    let m = 1000000007;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..windows {
        let hi = step(&mut seed);
        let a = ((hi * 32768 + step(&mut seed)) % (1000000 - 100000)) as usize;
        let r = max_rotate_function(&pool[a..a + 100000]);
        total += r;
        checksum = (checksum * 31 + r % m + m) % m;
    }
    println!("{} windows: total {}, checksum {}", windows, total, checksum);
}
