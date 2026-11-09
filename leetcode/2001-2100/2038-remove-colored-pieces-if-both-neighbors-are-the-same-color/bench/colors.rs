// LeetCode #2038: Remove Colored Pieces if Both Neighbors are the Same
// Color -- the ★ arm in Rust, the same algorithm and workload as
// colors.kara: the pieces collected into a `Vec<char>`, each player's moves
// counted, Alice winning with more.

fn winner_of_game(colors: String) -> bool {
    let c: Vec<char> = colors.chars().collect();
    let (mut alice, mut bob) = (0i64, 0i64);
    for i in 1..c.len().saturating_sub(1) {
        if c[i - 1] == c[i] && c[i] == c[i + 1] {
            if c[i] == 'A' {
                alice += 1;
            } else {
                bob += 1;
            }
        }
    }
    alice > bob
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2038;
    let mut rows: Vec<Vec<char>> = Vec::new();
    for r in 0..4 {
        let stay = [2, 3, 50, 1000][r];
        let mut c = if next_random(&mut seed) % 2 == 0 { 'A' } else { 'B' };
        let mut row: Vec<char> = Vec::new();
        for _ in 0..100000 {
            if next_random(&mut seed) % stay == 0 {
                c = if c == 'A' { 'B' } else { 'A' };
            }
            row.push(c);
        }
        rows.push(row);
    }
    let mut calls = 0;
    let mut wins: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..100 {
        for r in 0..4 {
            let at = (round * 7919 + r * 104729) % 100000;
            rows[r][at] = if rows[r][at] == 'A' { 'B' } else { 'A' };
            let colors: String = rows[r].iter().collect();
            let bit = if winner_of_game(colors) { 1 } else { 0 };
            calls += 1;
            wins += bit;
            check = (check * 3 + bit + 1) % 1000000007;
        }
    }
    println!("{} calls: Alice wins {}, checksum {}", calls, wins, check);
}
