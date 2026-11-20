// LeetCode #2410: Maximum Matching of Players With Trainers -- the bench,
// the ★ arm in Rust: both lists copied and sorted, each trainer upward
// taking the weakest player not yet matched if it is strong enough.

fn match_players_and_trainers(players: &[i64], trainers: &[i64]) -> i64 {
    let mut p = players.to_vec();
    let mut t = trainers.to_vec();
    p.sort();
    t.sort();
    let mut matched = 0usize;
    for &capacity in &t {
        if matched < p.len() && p[matched] <= capacity {
            matched += 1;
        }
    }
    matched as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2410;
    let mut cases: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for i in 0..10i64 {
        let players: Vec<i64> = (0..100000).map(|_| 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000).collect();
        let trainers: Vec<i64> = (0..100000)
            .map(|_| 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 900000000 + 10000000 * i)
            .collect();
        cases.push((players, trainers));
    }
    let mut check: i64 = 0;
    for p in 0..5 {
        for (players, trainers) in &cases {
            check = (check * 31 + match_players_and_trainers(players, trainers) + p) % 1000000007;
        }
    }
    println!("5 passes over 10 cases of 10^5 players and trainers: checksum {}", check);
}
