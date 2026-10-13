// Benchmark for #477: Rust mirror of the ★ arm (one bit at a time); see
// total_hamming_distance.kara.

fn total_hamming_distance(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut total = 0;
    for bit in 0..30 {
        let mut ones = 0;
        for &x in nums {
            ones += (x >> bit) & 1;
        }
        total += ones * (n - ones);
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 10000;
    let rounds = 5000;
    let mut seed: i64 = 477;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        nums.push((a * 32768 + b) % 1000000001);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        nums[r % n] = (a * 32768 + b) % 1000000001;
        let got = total_hamming_distance(&nums);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    println!("{} rounds on {} numbers: distances add up to {}, checksum {}", rounds, n, total, checksum);
}
