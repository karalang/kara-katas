// Benchmark for #442: mirror of find_duplicates.kara (marking by sign) on
// one random array of 1,000,000 numbers with 300,000 duplicates, built
// once, copied and searched 20 times over.

fn find_duplicates(mut nums: Vec<i64>) -> Vec<i64> {
    let mut duplicates: Vec<i64> = Vec::new();
    for i in 0..nums.len() {
        let x = nums[i].abs() as usize;
        if nums[x - 1] < 0 {
            duplicates.push(x as i64);
        } else {
            nums[x - 1] = -nums[x - 1];
        }
    }
    duplicates
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_index(seed: &mut i64, below: i64) -> i64 {
    (next_random(seed) * 32768 + next_random(seed)) % below
}

fn main() {
    let n: i64 = 1000000;
    let d: i64 = 300000;
    let rounds = 20;
    let mut seed: i64 = 442;
    // The first d of a shuffled 1..n twice, the next n - 2d once.
    let mut values: Vec<i64> = (1..n + 1).collect();
    for i in 0..n {
        let j = i + random_index(&mut seed, n - i);
        values.swap(i as usize, j as usize);
    }
    let mut nums: Vec<i64> = Vec::new();
    for i in 0..(n - d) as usize {
        nums.push(values[i]);
    }
    for i in 0..d as usize {
        nums.push(values[i]);
    }
    for i in 0..n {
        let j = i + random_index(&mut seed, n - i);
        nums.swap(i as usize, j as usize);
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let duplicates = find_duplicates(nums.clone());
        found += duplicates.len();
        for &x in &duplicates {
            checksum = (checksum * 31 + x + round) % 1000000007;
        }
    }
    println!("{} rounds on {} numbers: {} duplicates, checksum {}", rounds, n, found, checksum);
}
