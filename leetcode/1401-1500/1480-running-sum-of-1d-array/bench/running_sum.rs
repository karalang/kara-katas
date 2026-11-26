// LeetCode #1480: Running Sum of 1d Array -- bench, Rust mirror of
// running_sum.kara

fn running_sum(nums: &[i32]) -> Vec<i32> {
    let mut sums: Vec<i32> = Vec::new();
    let mut sum: i32 = 0;
    for &x in nums.iter() {
        sum += x;
        sums.push(sum);
    }
    sums
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1480;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..1000 {
        let nums: Vec<i32> = (0..1000)
            .map(|_| {
                let hi = next_random(&mut seed);
                ((hi * 32768 + next_random(&mut seed)) % 2000001 - 1000000) as i32
            })
            .collect();
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for pass in 0..200i64 {
        for p in 0..1000 {
            arrays[p][(check % 1000) as usize] = ((check / 7) % 2000001 - 1000000) as i32;
            let sums = running_sum(&arrays[p]);
            let mut s: i64 = 0;
            for (j, &x) in sums.iter().enumerate() {
                s += x as i64 * (j as i64 + 1);
            }
            check = (check * 31 + s % 1000000007 + 1000000007 + pass) % 1000000007;
        }
    }
    println!("200 passes over 1000 arrays of 1000 values: checksum {}", check);
}
