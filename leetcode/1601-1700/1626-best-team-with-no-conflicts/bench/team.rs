// LeetCode #1626: Best Team With No Conflicts -- the bench in Rust,
// mirroring team.kara: sorted by (age, score), the best team ending at
// each player from every earlier player scoring no higher.

fn best_team_score(scores: &[i32], ages: &[i32]) -> i32 {
    let mut players: Vec<(i32, i32)> = ages.iter().copied().zip(scores.iter().copied()).collect();
    players.sort();
    let n = players.len();
    let mut best: Vec<i64> = vec![0; n];
    for i in 0..n {
        let score = players[i].1 as i64;
        best[i] = score;
        for j in 0..i {
            if players[j].1 as i64 <= score {
                best[i] = best[i].max(best[j] + score);
            }
        }
    }
    *best.iter().max().unwrap() as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1626;
    let mut teams: Vec<(Vec<i32>, Vec<i32>)> = Vec::new();
    for _ in 0..100 {
        let mut scores = Vec::new();
        let mut ages = Vec::new();
        for _ in 0..1000 {
            let high = next_random(&mut seed);
            scores.push(((high * 32768 + next_random(&mut seed)) % 1000000 + 1) as i32);
            ages.push((next_random(&mut seed) % 1000 + 1) as i32);
        }
        teams.push((scores, ages));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (scores, ages) in &teams {
        let got = best_team_score(scores, ages) as i64;
        total += got;
        check = (check * 31 + got + 1) % 1000000007;
    }
    println!("100 teams of 1000 players: best scores sum to {total}, checksum {check}");
}
