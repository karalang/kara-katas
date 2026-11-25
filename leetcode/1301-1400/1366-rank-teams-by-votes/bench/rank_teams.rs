// LeetCode #1366 bench -- Rust: how many votes put each team in each place
// counted, and the teams sorted by those counts, then by letter.

fn rank_teams(votes: &[String]) -> String {
    let places = votes[0].len();
    let mut counts = vec![vec![0i64; places]; 26];
    for vote in votes {
        for (place, team) in vote.bytes().enumerate() {
            counts[(team - b'A') as usize][place] += 1;
        }
    }
    let mut teams: Vec<u8> = votes[0].bytes().collect();
    teams.sort_by(|a, b| {
        counts[(b - b'A') as usize]
            .cmp(&counts[(a - b'A') as usize])
            .then(a.cmp(b))
    });
    String::from_utf8(teams).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 elections of 1000 votes over all 26 teams, the constraints' most,
    // built once; then 3000 rounds, each swapping two places of one vote,
    // all drawn from the checksum so far, ranking that election and
    // folding the ranking into the checksum
    let mut seed = 1366i64;
    let mut elections: Vec<Vec<String>> = Vec::new();
    for _ in 0..20 {
        let mut votes = Vec::new();
        for _ in 0..1000 {
            let mut vote: Vec<u8> = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ".to_vec();
            for i in 1..26i64 {
                let j = next_random(&mut seed) % (i + 1);
                vote.swap(i as usize, j as usize);
            }
            votes.push(String::from_utf8(vote).unwrap());
        }
        elections.push(votes);
    }
    let mut check: i64 = 0;
    for r in 0..3000i64 {
        let e = (check % 20) as usize;
        let v = ((check / 20) % 1000) as usize;
        let (i, j) = (((check / 20000) % 26) as usize, ((check / 520000) % 26) as usize);
        let mut vote: Vec<u8> = elections[e][v].bytes().collect();
        vote.swap(i, j);
        elections[e][v] = String::from_utf8(vote).unwrap();
        let ranked = rank_teams(&elections[e]);
        for b in ranked.bytes() {
            check = (check * 31 + b as i64) % 1000000007;
        }
        check = (check + r) % 1000000007;
    }
    println!("3000 rounds over 20 elections of 1000 votes: checksum {}", check);
}
