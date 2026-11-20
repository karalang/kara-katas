// LeetCode #1732: Find the Highest Altitude -- the bench (altitude.kara):
// the altitudes listed, then the largest.

fn largest_altitude(gain: &[i32]) -> i32 {
    let mut altitudes: Vec<i32> = vec![0];
    for g in gain.iter() {
        altitudes.push(altitudes[altitudes.len() - 1] + g);
    }
    *altitudes.iter().max().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let rounds: i64 = 2000;
    let n = 100;
    let mut seed: i64 = 1732;
    let mut trips: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        let gain: Vec<i32> = (0..n)
            .map(|_| (next_random(&mut seed) % 201 - 100) as i32)
            .collect();
        trips.push(gain);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for gain in trips.iter() {
            let answer = largest_altitude(gain) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!(
        "{} trips of {} gains, {} rounds: highest points sum to {}, checksum {}",
        count, n, rounds, sum, check
    );
}
