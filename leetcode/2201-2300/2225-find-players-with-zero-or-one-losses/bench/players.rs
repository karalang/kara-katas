// LeetCode #2225: Find Players With Zero or One Losses -- the benchmark's
// Rust mirror of players.kara: a `HashMap` of losses, both lists sorted.

use std::collections::HashMap;

fn find_winners(matches: &[[i64; 2]]) -> Vec<Vec<i64>> {
    let mut losses: HashMap<i64, i64> = HashMap::new();
    for game in matches {
        if !losses.contains_key(&game[0]) {
            losses.insert(game[0], 0);
        }
        let before = *losses.get(&game[1]).unwrap_or(&0);
        losses.insert(game[1], before + 1);
    }
    let mut unbeaten = Vec::new();
    let mut once = Vec::new();
    for (&player, &count) in &losses {
        if count == 0 {
            unbeaten.push(player);
        } else if count == 1 {
            once.push(player);
        }
    }
    unbeaten.sort();
    once.sort();
    vec![unbeaten, once]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

// a match between two players of 1 to 10^5, never one against itself
fn draw_match(seed: &mut i64) -> [i64; 2] {
    let winner = wide_random(seed) % 100000 + 1;
    let mut loser = wide_random(seed) % 100000 + 1;
    if loser == winner {
        loser = winner % 100000 + 1;
    }
    [winner, loser]
}

fn main() {
    let mut seed = 2225;
    let mut tournaments: Vec<Vec<[i64; 2]>> = Vec::new();
    for _ in 0..4 {
        tournaments.push((0..100000).map(|_| draw_match(&mut seed)).collect());
    }
    let mut listed = 0;
    let mut check: i64 = 0;
    for _ in 0..25 {
        for t in 0..4 {
            // punch: one match is drawn again before each answer
            let at = (wide_random(&mut seed) % 100000) as usize;
            tournaments[t][at] = draw_match(&mut seed);
            for list in find_winners(&tournaments[t]) {
                listed += list.len();
                check = (check * 31 + list.len() as i64) % 1000000007;
                for p in list {
                    check = (check * 31 + p) % 1000000007;
                }
            }
        }
    }
    println!("100 tournaments: {listed} players listed in all, checksum {check}");
}
