// LeetCode #1560: Most Visited Sector in a Circular Track -- bench: the ★
// arm (the sectors from the first on to the last, wrapping past n) over
// 20000 tracks of up to 100 sectors and 100 legs, built once, each asked
// 100 times.
// Rust mirror of sectors.kara.

fn most_visited(n: i64, rounds: &[i64]) -> Vec<i64> {
    let start = rounds[0];
    let end = rounds[rounds.len() - 1];
    if start <= end {
        (start..=end).collect()
    } else {
        (1..=end).chain(start..=n).collect()
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1560;
    let mut tracks: Vec<(i64, Vec<i64>)> = Vec::new();
    for _ in 0..20000 {
        let n = next_random(&mut seed) % 99 + 2;
        let m = next_random(&mut seed) % 100 + 1;
        let mut rounds = vec![next_random(&mut seed) % n + 1];
        for _ in 0..m {
            let at = rounds[rounds.len() - 1];
            rounds.push((at - 1 + next_random(&mut seed) % (n - 1) + 1) % n + 1);
        }
        tracks.push((n, rounds));
    }
    let mut check = 0;
    let mut total = 0;
    for pass in 0..100i64 {
        for (t, (n, rounds)) in tracks.iter().enumerate() {
            let sectors = most_visited(*n, rounds);
            total += sectors.len();
            check = mix(check, sectors[((pass * 7 + t as i64) as usize) % sectors.len()]);
        }
    }
    println!("100 passes over 20000 tracks: {} sectors, checksum {}", total, check);
}
