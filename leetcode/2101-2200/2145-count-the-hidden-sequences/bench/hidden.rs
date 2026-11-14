// LeetCode #2145: Count the Hidden Sequences -- the benchmark, the same
// algorithm as hidden.kara.

fn number_of_arrays(differences: &[i64], lower: i64, upper: i64) -> i64 {
    let mut at = 0;
    let mut lowest = 0;
    let mut highest = 0;
    for &d in differences {
        at += d;
        lowest = lowest.min(at);
        highest = highest.max(at);
    }
    ((upper - lower) - (highest - lowest) + 1).max(0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2145;
    let mut walks: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let walk: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 21 - 10).collect();
        walks.push(walk);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..200 {
        for w in 0..20 {
            let hi = next_random(&mut seed);
            let at = ((hi * 32768 + next_random(&mut seed)) % 100000) as usize;
            walks[w][at] = next_random(&mut seed) % 21 - 10;
            let count = number_of_arrays(&walks[w], -100000, 100000);
            total += count;
            check = (check * 31 + count + round) % 1000000007;
        }
    }
    println!("4000 solves: {} sequences in all, checksum {}", total, check);
}
