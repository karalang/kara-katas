// LeetCode #1109: Corporate Flight Bookings -- the bench in Rust: the ★
// arm (a difference array and a running total) over 16 problems of
// 2 * 10^4 flights and 2 * 10^4 bookings, each round changing one booking
// in every problem and solving it again.

fn corp_flight_bookings(bookings: &Vec<Vec<i64>>, n: i64) -> Vec<i64> {
    let mut change: Vec<i64> = vec![0; n as usize + 1];
    for b in bookings.iter() {
        change[(b[0] - 1) as usize] += b[2];
        change[b[1] as usize] -= b[2];
    }
    let mut seats: Vec<i64> = Vec::with_capacity(n as usize);
    let mut running = 0;
    for i in 0..n as usize {
        running += change[i];
        seats.push(running);
    }
    seats
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn booking(seed: &mut i64, n: i64) -> Vec<i64> {
    let a = next_random(seed) % n + 1;
    let b = next_random(seed) % n + 1;
    vec![a.min(b), a.max(b), next_random(seed) % 10000 + 1]
}

fn main() {
    let n = 20000;
    let mut seed = 1109;
    let mut problems: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..16 {
        let bookings: Vec<Vec<i64>> = (0..20000).map(|_| booking(&mut seed, n)).collect();
        problems.push(bookings);
    }
    let mut busiest: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..200usize {
        for j in 0..problems.len() {
            let at = (round * 7919 + j * 104729) % 20000;
            problems[j][at] = booking(&mut seed, n);
            let seats = corp_flight_bookings(&problems[j], n);
            busiest += *seats.iter().max().unwrap();
            check = (check * 31 + seats[(round * 31 + j) % n as usize]) % 1000000007;
        }
    }
    println!("200 rounds over 16 problems of 20000 flights: busiest total {}, checksum {}", busiest, check);
}
