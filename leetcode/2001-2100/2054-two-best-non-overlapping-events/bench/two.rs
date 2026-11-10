// LeetCode #2054: Two Best Non-Overlapping Events -- Rust mirror of the ★
// arm's benchmark (two.kara): the same 50 sets of 100000 events, the same
// stable sort by start, best value from each event on, and
// `partition_point` for each event.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn max_two_events(events: &[(i64, i64, i64)]) -> i64 {
    let mut events = events.to_vec();
    events.sort();
    let n = events.len();
    let mut best_from = vec![0i64; n + 1];
    for i in (0..n).rev() {
        best_from[i] = best_from[i + 1].max(events[i].2);
    }
    let mut best = 0;
    for &(_, end, value) in &events {
        let next = events.partition_point(|e| e.0 <= end);
        best = best.max(value + best_from[next]);
    }
    best
}

fn main() {
    let mut seed = 2054;
    let mut total = 0i64;
    let mut check = 0i64;
    for t in 0..50 {
        let longest = [1000, 1000000, 100000000, 500000000][t % 4];
        let span = 1000000000 - longest;
        let mut events: Vec<(i64, i64, i64)> = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            let start = (hi * 32768 + next_random(&mut seed)) % span + 1;
            let hi = next_random(&mut seed);
            let end = start + (hi * 32768 + next_random(&mut seed)) % longest;
            let hi = next_random(&mut seed);
            let value = (hi * 32768 + next_random(&mut seed)) % 1000000 + 1;
            events.push((start, end, value));
        }
        let best = max_two_events(&events);
        total += best;
        check = (check * 31 + best) % 1000000007;
    }
    println!("50 sets: sum {total}, checksum {check}");
}
