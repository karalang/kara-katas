// Benchmark for #462: mirror of min_moves2.kara (the ★ arm: sort, take
// the median) on the same workload. The sort is the standard library's
// stable sort.

fn min_moves2(nums: Vec<i64>) -> i64 {
    let mut sorted = nums;
    sorted.sort();
    let median = sorted[sorted.len() / 2];
    let mut moves = 0;
    for x in sorted {
        moves += (x - median).abs();
    }
    moves
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_number(seed: &mut i64) -> i64 {
    let spread = 1000000000;
    ((next_random(seed) * 32768 + next_random(seed)) * 32768 + next_random(seed)) % (2 * spread + 1) - spread
}

fn main() {
    let n: i64 = 1000000;
    let rounds = 10;
    let mut seed: i64 = 462;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(random_number(&mut seed));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let k = (next_random(&mut seed) * 65536 + next_random(&mut seed)) % n;
        nums[k as usize] = random_number(&mut seed);
        let moves = min_moves2(nums.clone());
        total += moves;
        checksum = (checksum * 31 + moves % 1000003) % 1000000007;
    }
    println!("{} rounds on {} numbers: {} moves in all, checksum {}", rounds, n, total, checksum);
}
