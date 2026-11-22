// LeetCode #2739: Total Distance Traveled -- the bench (distance.kara in
// Rust): (m - 1) / 4 transfers, as many as the additional tank holds.

fn distance_traveled(main_tank: i64, additional_tank: i64) -> i64 {
    let transfers = ((main_tank - 1) / 4).min(additional_tank);
    (main_tank + transfers) * 10
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 1000000;
    let rounds: i64 = 100;
    let mut seed = 2739;
    let mut tanks: Vec<(i64, i64)> = Vec::new();
    for _ in 0..count {
        let m = next_random(&mut seed) % 100 + 1;
        let a = next_random(&mut seed) % 100 + 1;
        tanks.push((m, a));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(m, a) in tanks.iter() {
            let d = distance_traveled(m, a);
            sum += d;
            check = (check * 31 + d + r) % 1000000007;
        }
    }
    println!("{} pairs of tanks, {} rounds: distances sum to {}, checksum {}", count, rounds, sum, check);
}
