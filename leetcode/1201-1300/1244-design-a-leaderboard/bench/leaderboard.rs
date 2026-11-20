// LeetCode #1244 bench, in Rust: the ★ arm (each player's total in a
// `HashMap`; a top sorts the totals from the highest and adds the first
// k) on 100 sessions of 3000 random calls on players up to 10000; the
// tops' answers folded into a checksum.

use std::collections::HashMap;

struct Leaderboard {
    scores: HashMap<i64, i64>,
}

impl Leaderboard {
    fn new() -> Self {
        Leaderboard { scores: HashMap::new() }
    }

    fn add_score(&mut self, player_id: i64, score: i64) {
        let now = *self.scores.get(&player_id).unwrap_or(&0);
        self.scores.insert(player_id, now + score);
    }

    fn top(&self, k: i64) -> i64 {
        let mut all: Vec<i64> = self.scores.values().copied().collect();
        all.sort_by(|a, b| b.cmp(a));
        all.iter().take(k as usize).sum()
    }

    fn reset(&mut self, player_id: i64) {
        self.scores.remove(&player_id);
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn session(calls: i64, players: i64, seed: &mut i64) -> (i64, i64) {
    let mut board = Leaderboard::new();
    let mut on: Vec<i64> = Vec::new();
    let mut check = 0;
    let mut tops = 0;
    for _ in 0..calls {
        let op = next_random(seed) % 4;
        if op <= 1 || on.is_empty() {
            let player = next_random(seed) % players + 1;
            let score = next_random(seed) % 100 + 1;
            board.add_score(player, score);
            if !on.contains(&player) {
                on.push(player);
            }
        } else if op == 2 {
            let k = next_random(seed) % on.len() as i64 + 1;
            let got = board.top(k);
            check = (check * 131 + got) % 1000000007;
            tops += 1;
        } else {
            let i = (next_random(seed) % on.len() as i64) as usize;
            let player = on.swap_remove(i);
            board.reset(player);
        }
    }
    (tops, check)
}

fn main() {
    let mut seed = 1244;
    let mut tops = 0;
    let mut check = 0;
    for _ in 0..100 {
        let (t, c) = session(3000, 10000, &mut seed);
        tops += t;
        check = (check * 31 + c) % 1000000007;
    }
    println!("100 sessions of 3000 calls on 10000 players: {tops} tops, checksum {check}");
}
