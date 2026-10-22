// Benchmark for #849: Maximize Distance to Closest Person -- Rust twin of
// the Kāra ★ arm (one pass, remembering the last person).

fn max_dist_to_closest(seats: &[i64]) -> i64 {
    let n = seats.len() as i64;
    let mut last: i64 = -1;
    let mut best: i64 = 0;
    for i in 0..n {
        if seats[i as usize] == 1 {
            if last < 0 {
                best = i;
            } else {
                best = best.max((i - last) / 2);
            }
            last = i;
        }
    }
    best.max(n - 1 - last)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds = 20000;
    let n: i64 = 20000;
    let mut seed: i64 = 849;
    let mut rows: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let odds = 2i64 << (g % 8);
        let mut seats: Vec<i64> = Vec::new();
        for _ in 0..n {
            seats.push(if next_random(&mut seed) % odds == 0 { 1 } else { 0 });
        }
        let taken = next_random(&mut seed) % n;
        let empty = (taken + 1 + next_random(&mut seed) % (n - 1)) % n;
        seats[taken as usize] = 1;
        seats[empty as usize] = 0;
        rows.push(seats);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let d = max_dist_to_closest(&rows[round % count]);
        total += d;
        checksum = (checksum * 31 + d) % 1000000007;
    }
    println!("{} rounds of {} rows: distances sum to {}, checksum {}", rounds, count, total, checksum);
}
