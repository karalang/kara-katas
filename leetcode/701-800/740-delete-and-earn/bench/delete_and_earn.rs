// LeetCode #740: Delete and Earn -- house robber over values.
// Benchmark mirror of the Kara star arm: total the points each value is
// worth in a table as long as the largest value, then walk the values
// in order keeping the best total with the last value taken and with
// it left.

fn delete_and_earn(nums: &Vec<i64>) -> i64 {
    let mut top = 0;
    for x in nums.iter() {
        if *x > top {
            top = *x;
        }
    }
    let mut points: Vec<i64> = Vec::new();
    for _ in 0..top + 1 {
        points.push(0);
    }
    for x in nums.iter() {
        points[*x as usize] += *x;
    }
    let mut take = 0;
    let mut skip = 0;
    for v in 0..(top + 1) as usize {
        let taken = skip + points[v];
        skip = if take > skip { take } else { skip };
        take = taken;
    }
    if take > skip { take } else { skip }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 740;
    let n: i64 = 20000;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(1 + next_random(&mut seed) % 10000);
    }
    let mut total: i64 = 0;
    for _ in 0..5000 {
        for _ in 0..20 {
            let j = (next_random(&mut seed) % n) as usize;
            nums[j] = 1 + next_random(&mut seed) % 10000;
        }
        total += delete_and_earn(&nums);
    }
    println!("5000 rounds of 20000 numbers: {} points in all", total);
}
