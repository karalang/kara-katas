// Benchmark for #461: mirror of hamming_distance.kara (the ★ arm, clearing
// the lowest set bit) on the same workload.

fn hamming_distance(x: i64, y: i64) -> i64 {
    let mut z = x ^ y;
    let mut count = 0;
    while z != 0 {
        z &= z - 1;
        count += 1;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random31(seed: &mut i64) -> i64 {
    ((next_random(seed) * 32768 + next_random(seed)) * 2 + next_random(seed) % 2) % 2147483648
}

fn main() {
    let n: i64 = 1000000;
    let rounds = 20;
    let mut seed: i64 = 461;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(random31(&mut seed));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let k = (next_random(&mut seed) * 65536 + next_random(&mut seed)) % n;
        nums[k as usize] = random31(&mut seed);
        let mut sum = 0;
        for i in 1..n as usize {
            sum += hamming_distance(nums[i - 1], nums[i]);
        }
        total += sum;
        checksum = (checksum * 31 + sum) % 1000000007;
    }
    println!("{} rounds on {} numbers: total distance {}, checksum {}", rounds, n, total, checksum);
}
