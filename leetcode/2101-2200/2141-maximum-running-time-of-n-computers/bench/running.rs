// LeetCode #2141: Maximum Running Time of N Computers -- the benchmark, the
// same algorithm as running.kara.

fn max_run_time(n: i64, batteries: &[i64]) -> i64 {
    let total: i64 = batteries.iter().sum();
    let mut low = 0;
    let mut high = total / n;
    while low < high {
        let mid = (low + high + 1) / 2;
        let usable: i64 = batteries.iter().map(|&b| b.min(mid)).sum();
        if usable >= n * mid {
            low = mid;
        } else {
            high = mid - 1;
        }
    }
    low
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2141;
    let mut fleets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut batteries = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            batteries.push((hi * 32768 + next_random(&mut seed)) % 1000000000 + 1);
        }
        fleets.push(batteries);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..20 {
        for f in 0..10 {
            let hi = next_random(&mut seed);
            let at = ((hi * 32768 + next_random(&mut seed)) % 100000) as usize;
            let hi = next_random(&mut seed);
            fleets[f][at] = (hi * 32768 + next_random(&mut seed)) % 1000000000 + 1;
            let minutes = max_run_time(10000 * (f as i64 + 1), &fleets[f]);
            total += minutes;
            check = (check * 31 + minutes % 1000000007 + round) % 1000000007;
        }
    }
    println!("200 solves: {} minutes in all, checksum {}", total, check);
}
