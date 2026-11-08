// LeetCode #2029: Stone Game IX -- the ★ arm in Rust, the same algorithm and
// workload as stones.kara.

fn stone_game_ix(stones: &[i64]) -> bool {
    let mut cnt = [0i64; 3];
    for &s in stones {
        cnt[(s % 3) as usize] += 1;
    }
    if cnt[0] % 2 == 0 {
        cnt[1] >= 1 && cnt[2] >= 1
    } else {
        (cnt[1] - cnt[2]).abs() > 2
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2029;
    let mut games: Vec<Vec<i64>> = Vec::new();
    for a in 0..20i64 {
        let mut stones = Vec::new();
        for _ in 0..100000 {
            let base = 3 * (next_random(&mut seed) % 3333);
            let residue = if next_random(&mut seed) % 10 < a % 5 {
                3
            } else if next_random(&mut seed) % 10 < 3 * a % 11 {
                1
            } else {
                2
            };
            stones.push(base + residue);
        }
        games.push(stones);
    }
    let (mut calls, mut wins, mut check) = (0i64, 0i64, 0i64);
    for round in 0..100usize {
        for a in 0..20usize {
            games[a][(round * 997 + a * 31) % 100000] += 1;
            let answer = stone_game_ix(&games[a]);
            calls += 1;
            if answer {
                wins += 1;
            }
            check = (check * 31 + if answer { 1 } else { 2 }) % 1000000007;
        }
    }
    println!("{} calls: Alice wins {}, checksum {}", calls, wins, check);
}
